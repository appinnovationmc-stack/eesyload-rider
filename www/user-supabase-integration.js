/* ─── SUPABASE CLIENT (Rider App) ───────────────────────── */
const SUPABASE_URL = 'https://mbtqqnbklcltrtwlpduq.supabase.co';
const SUPABASE_ANON_KEY = 'sb_publishable_ff0SBElpjzVkCaHyPHAYUQ_1sOCyRES';
const sb = supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);

/* ─── AUTH ───────────────────────────────────────────────── */
async function sbSendOtp(phone) {
  const { error } = await sb.auth.signInWithOtp({ phone });
  if (error) throw error;
}

async function sbVerifyOtp(phone, token) {
  const { data, error } = await sb.auth.verifyOtp({ phone, token, type: 'sms' });
  if (error) throw error;
  const { data: existing } = await sb.from('profiles').select('id').eq('id', data.user.id).single();
  if (!existing) {
    await sb.from('profiles').insert({ id: data.user.id, role: 'rider', phone });
  }
  return data.user;
}

async function sbUpdateRiderName(fullName) {
  const user = await sbGetCurrentUser();
  const { error } = await sb.from('profiles').update({ full_name: fullName }).eq('id', user.id);
  if (error) throw error;
  return true;
}

async function sbGetCurrentUser() {
  const { data } = await sb.auth.getUser();
  return data.user;
}

async function sbSignOut() {
  const { error } = await sb.auth.signOut();
  if (error) throw error;
}

/* ─── REFERRALS ──────────────────────────────────────────── */
async function getMyReferralCode() {
  const user = await sbGetCurrentUser();
  if (!user) throw new Error('Not signed in');
  const { data, error } = await sb.from('profiles')
    .select('referral_code,referred_by').eq('id', user.id).single();
  if (error) throw error;
  return data;
}

async function applyReferralCode(code) {
  const user = await sbGetCurrentUser();
  if (!user) throw new Error('Not signed in');

  const { data: ownerId, error: rpcError } = await sb.rpc('resolve_referral_code', { code });
  if (rpcError) throw rpcError;
  if (!ownerId) throw new Error('That referral code was not found.');
  if (ownerId === user.id) throw new Error("You can't use your own referral code.");

  const { error } = await sb.from('profiles')
    .update({ referred_by: ownerId }).eq('id', user.id);
  if (error) throw error;
  return true;
}

/* ─── VEHICLE TYPES & ADD-ONS (real pricing) ──────────────── */
async function getVehicleTypes() {
  const { data, error } = await sb.from('vehicle_types')
    .select('*').eq('active', true).order('sort_order');
  if (error) throw error;
  return data;
}

async function getServiceAddons() {
  const { data, error } = await sb.from('service_addons')
    .select('*').eq('active', true).order('sort_order');
  if (error) throw error;
  return data;
}

/* ─── SAVED ADDRESSES ────────────────────────────────────── */
async function getSavedAddresses() {
  const user = await sbGetCurrentUser();
  if (!user) throw new Error('Not signed in');
  const { data, error } = await sb.from('saved_addresses')
    .select('*').eq('rider_id', user.id)
    .order('created_at', { ascending: true });
  if (error) throw error;
  return data;
}

async function saveAddress(label, formattedAddress, lat, lng) {
  const user = await sbGetCurrentUser();
  if (!user) throw new Error('Not signed in');
  const { data, error } = await sb.from('saved_addresses')
    .upsert({
      rider_id: user.id,
      label,
      formatted_address: formattedAddress,
      lat: lat || null,
      lng: lng || null,
    }, { onConflict: 'rider_id,label' })
    .select().single();
  if (error) throw error;
  return data;
}

/* ─── DRIVER LIVE LOCATION (for rider tracking map) ───────── */
async function getDriverLocation(driverId) {
  const { data, error } = await sb.from('driver_locations')
    .select('lat,lng,heading,updated_at')
    .eq('driver_id', driverId)
    .single();
  if (error) return null; // no location yet, or RLS blocked (no active booking together)
  return data;
}

function subscribeToDriverLocation(driverId, onUpdate) {
  return sb.channel('driver-location-'+driverId)
    .on('postgres_changes', {
      event: '*', schema: 'public', table: 'driver_locations', filter: 'driver_id=eq.'+driverId
    }, (payload) => onUpdate(payload.new))
    .subscribe();
}

/* ─── BOOKINGS ───────────────────────────────────────────── */
async function createBooking(booking) {
  const { data: sess } = await sb.auth.getSession();
  const token = sess?.session?.access_token;
  if (!token) throw new Error('Not signed in');

  const res = await fetch(SUPABASE_URL + '/functions/v1/verify-and-create-booking', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer ' + token,
      'apikey': SUPABASE_ANON_KEY,
    },
    body: JSON.stringify({
      pickup_address: booking.pickup_address,
      dropoff_address: booking.dropoff_address,
      vehicle_type_id: booking.vehicle_type_id,
      addon_ids: (booking.addons || []).map(a => a.id).filter(Boolean),
      claimed_total_fare: booking.total_fare,
      paystack_reference: booking.paystack_reference || null,
    }),
  });

  const result = await res.json();
  if (!res.ok) {
    throw new Error(result.error || 'Could not create booking');
  }
  return result.booking;
}

async function getChatMessages(bookingId) {
  const { data, error } = await sb.from('booking_messages')
    .select('id, sender_id, body, created_at')
    .eq('booking_id', bookingId)
    .order('created_at', { ascending: true });
  if (error) throw error;
  return data;
}

async function sendChatMessage(bookingId, body) {
  const user = await sbGetCurrentUser();
  if (!user) throw new Error('Not signed in');
  const { data, error } = await sb.from('booking_messages')
    .insert({ booking_id: bookingId, sender_id: user.id, body })
    .select().single();
  if (error) throw error;
  return data;
}

function subscribeToChatMessages(bookingId, onMessage) {
  return sb.channel('chat-' + bookingId)
    .on('postgres_changes', {
      event: 'INSERT', schema: 'public', table: 'booking_messages', filter: 'booking_id=eq.' + bookingId
    }, (payload) => onMessage(payload.new))
    .subscribe();
}

function subscribeToBookingUpdates(bookingId, onUpdate) {
  return sb.channel('booking-'+bookingId)
    .on('postgres_changes', {
      event: 'UPDATE', schema: 'public', table: 'bookings', filter: 'id=eq.'+bookingId
    }, (payload) => onUpdate(payload.new))
    .subscribe();
}

async function getDriverProfile(driverId) {
  const { data, error } = await sb.from('profiles').select('full_name,vehicle_type,vehicle_plate,avatar_url,phone').eq('id', driverId).single();
  if (error) throw error;
  return data;
}

async function getRiderProfile() {
  const user = await sbGetCurrentUser();
  if (!user) throw new Error('Not signed in');
  const { data, error } = await sb.from('profiles').select('full_name,phone,avatar_url').eq('id', user.id).single();
  if (error) throw error;
  return data;
}

async function cancelBookingAsRider(bookingId) {
  const { error } = await sb.from('bookings').update({ status: 'cancelled_rider' }).eq('id', bookingId);
  if (error) throw error;
}

async function getRiderBookings() {
  const user = await sbGetCurrentUser();
  if (!user) throw new Error('Not signed in');
  const { data, error } = await sb.from('bookings')
    .select('*').eq('rider_id', user.id)
    .in('status', ['delivered','cancelled_rider','cancelled_driver'])
    .order('created_at', { ascending: false });
  if (error) throw error;
  return data;
}


async function handleAvatarUpload(event) {
  const file = event.target.files[0];
  if (!file) return;
  const statusEl = document.getElementById('editProfileStatus');
  if (statusEl) statusEl.textContent = 'Uploading...';
  try {
    const { data: { user } } = await sb.auth.getUser();
    if (!user) throw new Error('Not signed in');
    const ext = file.name.split('.').pop();
    const path = `${user.id}/avatar.${ext}`;
    const { error: uploadError } = await sb.storage.from('avatars').upload(path, file, { upsert: true });
    if (uploadError) throw uploadError;
    const { data: urlData } = sb.storage.from('avatars').getPublicUrl(path);
    const avatarUrl = urlData.publicUrl + '?t=' + Date.now();
    const { error: updateError } = await sb.from('profiles').update({ avatar_url: avatarUrl }).eq('id', user.id);
    if (updateError) throw updateError;
    const imgEl = document.getElementById('editAvatarImg');
    if (imgEl) imgEl.src = avatarUrl;
    if (statusEl) statusEl.textContent = 'Photo updated';
  } catch (err) {
    console.error('Avatar upload failed:', err);
    if (statusEl) statusEl.textContent = 'Upload failed \u2014 try again';
  }
}

async function saveEditProfile() {
  const nameInput = document.getElementById('editNameInput');
  const statusEl = document.getElementById('editProfileStatus');
  const newName = nameInput ? nameInput.value.trim() : '';
  if (!newName) {
    if (statusEl) statusEl.textContent = 'Name cannot be empty';
    return;
  }
  if (statusEl) statusEl.textContent = 'Saving...';
  try {
    await sbUpdateRiderName(newName);
    const profNameEl = document.getElementById('profName');
    if (profNameEl) profNameEl.textContent = newName;
    if (statusEl) statusEl.textContent = 'Saved';
    setTimeout(() => go('profile'), 500);
  } catch (err) {
    console.error('Save profile failed:', err);
    if (statusEl) statusEl.textContent = 'Save failed \u2014 try again';
  }
}

async function openEditProfile() {
  try {
    const profile = await getRiderProfile();
    const nameInput = document.getElementById('editNameInput');
    const imgEl = document.getElementById('editAvatarImg');
    const phoneEl = document.getElementById('editPhoneDisplay');
    if (nameInput) nameInput.value = (profile && profile.full_name) || '';
    if (imgEl) imgEl.src = (profile && profile.avatar_url) || '';
    if (phoneEl) phoneEl.textContent = (profile && profile.phone) ? ('+' + profile.phone) : '—';
  } catch (err) {
    console.error('Failed to load profile for editing:', err);
  }
}


async function sbRequestPhoneChange(newPhone) {
  const { error } = await sb.auth.updateUser({ phone: newPhone });
  if (error) throw error;
}

async function sbVerifyPhoneChange(newPhone, token) {
  const { data, error } = await sb.auth.verifyOtp({ phone: newPhone, token, type: 'phone_change' });
  if (error) throw error;
  const cleanPhone = newPhone.replace(/^\+/, '');
  const { error: profileError } = await sb.from('profiles').update({ phone: cleanPhone }).eq('id', data.user.id);
  if (profileError) throw profileError;
  return data;
}


async function sbLogSosAlert(lat, lng, locationError) {
  const user = await sbGetCurrentUser();
  if (!user) throw new Error('Not signed in');
  const bookingId = (typeof AppState !== 'undefined' && AppState.currentBookingId) ? AppState.currentBookingId : null;
  const { error } = await sb.from('sos_alerts').insert({
    rider_id: user.id,
    booking_id: bookingId,
    lat: lat,
    lng: lng,
    location_error: !!locationError
  });
  if (error) throw error;
}
