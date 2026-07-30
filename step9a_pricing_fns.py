with open('user-supabase-integration.js', 'r') as f:
    content = f.read()

marker = "/* ─── SAVED ADDRESSES ────────────────────────────────────── */"

addition = """/* ─── VEHICLE TYPES & ADD-ONS (real pricing) ──────────────── */
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

""" + marker

if marker not in content:
    print("ERROR: marker not found")
else:
    content = content.replace(marker, addition, 1)
    with open('user-supabase-integration.js', 'w') as f:
        f.write(content)
    print("SUCCESS: getVehicleTypes and getServiceAddons added")
