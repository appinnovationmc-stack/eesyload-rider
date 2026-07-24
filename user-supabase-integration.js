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

async function sbGetCurrentUser() {
  const { data } = await sb.auth.getUser();
  return data.user;
}

async function sbSignOut() {
  const { error } = await sb.auth.signOut();
  if (error) throw error;
}

/* ─── BOOKINGS ───────────────────────────────────────────── */
async function createBooking(booking) {
  const user = await sbGetCurrentUser();
  if (!user) throw new Error('Not signed in');
  const { data, error } = await sb.from('bookings').insert({
    rider_id: user.id,
    pickup_address: booking.pickup_address,
    dropoff_address: booking.dropoff_address,
    vehicle_name: booking.vehicle_name,
    base_fare: booking.base_fare,
    total_fare: booking.total_fare,
    addons: booking.addons || [],
    addons_total: booking.addons_total || 0,
    status: 'pending',
  }).select().single();
  if (error) throw error;
  return data;
}

function subscribeToBookingUpdates(bookingId, onUpdate) {
  return sb.channel('booking-'+bookingId)
    .on('postgres_changes', {
      event: 'UPDATE', schema: 'public', table: 'bookings', filter: 'id=eq.'+bookingId
    }, (payload) => onUpdate(payload.new))
    .subscribe();
}

async function getDriverProfile(driverId) {
  const { data, error } = await sb.from('profiles').select('full_name,vehicle_type,vehicle_plate').eq('id', driverId).single();
  if (error) throw error;
  return data;
}

async function cancelBookingAsRider(bookingId) {
  const { error } = await sb.from('bookings').update({ status: 'cancelled_rider' }).eq('id', bookingId);
  if (error) throw error;
}
