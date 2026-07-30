with open('index.html', 'r') as f:
    content = f.read()

old = """    const booking=await createBooking({
      pickup_address: AppState.pickup,
      dropoff_address: AppState.dropoff,
      vehicle_name: AppState.vehicleName,
      base_fare: AppState.vehiclePrice,
      total_fare: calcFare(),
      addons: AppState.addons,
      addons_total: AppState.addons.reduce((s,a)=>s+a.price,0),
      paystack_reference: window._pendingPaystackRef || null
    });"""

new = """    const booking=await createBooking({
      pickup_address: AppState.pickup,
      dropoff_address: AppState.dropoff,
      vehicle_name: AppState.vehicleName,
      vehicle_type_id: AppState.vehicleTypeId,
      base_fare: AppState.vehiclePrice,
      total_fare: calcFare(),
      addons: AppState.addons,
      addons_total: AppState.addons.reduce((s,a)=>s+a.price,0),
      paystack_reference: window._pendingPaystackRef || null
    });"""

if old not in content:
    print("ERROR: exact match not found")
else:
    content = content.replace(old, new, 1)
    with open('index.html', 'w') as f:
        f.write(content)
    print("SUCCESS: vehicle_type_id added to booking call")
