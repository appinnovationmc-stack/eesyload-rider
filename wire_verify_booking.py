with open('user-supabase-integration.js', 'r') as f:
    content = f.read()

old = """async function createBooking(booking) {
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
    paystack_reference: booking.paystack_reference || null,
    payout_status: booking.paystack_reference ? 'paid' : 'unpaid',
  }).select().single();
  if (error) throw error;
  return data;
}"""

new = """async function createBooking(booking) {
  const { data: sess } = await sb.auth.getSession();
  const token = sess?.session?.access_token;
  if (!token) throw new Error('Not signed in');

  const res = await fetch(SUPABASE_URL + '/functions/v1/verify-and-create-booking', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer ' + token,
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
}"""

if old not in content:
    print("ERROR: exact match not found")
else:
    content = content.replace(old, new, 1)
    with open('user-supabase-integration.js', 'w') as f:
        f.write(content)
    print("SUCCESS: createBooking now uses server-side fare verification")
