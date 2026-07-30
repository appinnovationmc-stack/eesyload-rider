with open('user-supabase-integration.js', 'r') as f:
    content = f.read()

marker = "/* ─── DRIVER LIVE LOCATION (for rider tracking map) ───────── */"

addition = """/* ─── SAVED ADDRESSES ────────────────────────────────────── */
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

""" + marker

if marker not in content:
    print("ERROR: marker not found")
else:
    content = content.replace(marker, addition, 1)
    with open('user-supabase-integration.js', 'w') as f:
        f.write(content)
    print("SUCCESS: saved address functions added")
