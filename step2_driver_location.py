with open('user-supabase-integration.js', 'r') as f:
    content = f.read()

marker = "/* ─── BOOKINGS ───────────────────────────────────────────── */"

addition = """/* ─── DRIVER LIVE LOCATION (for rider tracking map) ───────── */
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

""" + marker

if marker not in content:
    print("ERROR: marker not found")
else:
    content = content.replace(marker, addition, 1)
    with open('user-supabase-integration.js', 'w') as f:
        f.write(content)
    print("SUCCESS: driver location functions added")
