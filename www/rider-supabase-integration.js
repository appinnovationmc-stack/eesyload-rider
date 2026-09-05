const SUPABASE_URL = 'https://mbtqqnbklcltrtwlpduq.supabase.co';
const SUPABASE_ANON_KEY = 'sb_publishable_ff0SBElpjzVkCaHyPHAYUQ_1sOCyRES';
const sb = supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);

async function sbSendOtp(phone) {
  const { error } = await sb.auth.signInWithOtp({ phone });
  if (error) throw error;
}

async function sbVerifyOtp(phone, token) {
  const { data, error } = await sb.auth.verifyOtp({ phone, token, type: 'sms' });
  if (error) throw error;
  const user = data.user;
  const { data: existing } = await sb.from('profiles').select('id').eq('id', user.id).maybeSingle();
  if (!existing) {
    await sb.from('profiles').insert({ id: user.id, role: 'rider', phone });
  }
  return user;
}

async function sbGetCurrentUser() {
  const { data } = await sb.auth.getUser();
  return data.user;
}

async function sbSignOut() {
  const { error } = await sb.auth.signOut();
  if (error) throw error;
}

async function createRiderBooking({
  pickup_address, dropoff_address, vehicle_name,
  pickup_lat, pickup_lng, dropoff_lat, dropoff_lng,
  total_fare, notes
}) {
  const user = await sbGetCurrentUser();
  if (!user) throw new Error('Sign in to book');
  const payload = {
    rider_id: user.id,
    status: 'pending',
    pickup_address,
    dropoff_address,
    vehicle_name,
    pickup_lat: pickup_lat != null ? Number(pickup_lat) : null,
    pickup_lng: pickup_lng != null ? Number(pickup_lng) : null,
    dropoff_lat: dropoff_lat != null ? Number(dropoff_lat) : null,
    dropoff_lng: dropoff_lng != null ? Number(dropoff_lng) : null,
    total_fare: Number(total_fare) || 0,
    notes: notes || null,
    driver_id: null
  };
  const { data, error } = await sb.from('bookings').insert(payload).select().single();
  if (error) throw error;
  return data;
}

async function getMyRiderBookings() {
  const user = await sbGetCurrentUser();
  if (!user) return [];
  const { data, error } = await sb.from('bookings')
    .select('*')
    .eq('rider_id', user.id)
    .order('created_at', { ascending: false });
  if (error) throw error;
  return data || [];
}

function subscribeToMyBooking(bookingId, onUpdate) {
  return sb.channel('rider-booking-' + bookingId)
    .on('postgres_changes', {
      event: 'UPDATE', schema: 'public', table: 'bookings', filter: 'id=eq.' + bookingId
    }, (payload) => onUpdate(payload.new))
    .subscribe();
}
