with open('index.html', 'r') as f:
    content = f.read()

old = """          const driver=await getDriverProfile(updated.driver_id);
          AppState.driver={
            name: driver.full_name||'Your driver',
            vehicle: (driver.vehicle_type||'')+(driver.vehicle_plate?(' · '+driver.vehicle_plate):''),
            avatarUrl: driver.avatar_url||null,
            rating: 5.0,
            loads: 0
          };"""

new = """          const driver=await getDriverProfile(updated.driver_id);
          AppState.driver={
            id: updated.driver_id,
            name: driver.full_name||'Your driver',
            vehicle: (driver.vehicle_type||'')+(driver.vehicle_plate?(' · '+driver.vehicle_plate):''),
            avatarUrl: driver.avatar_url||null,
            rating: 5.0,
            loads: 0
          };"""

if old not in content:
    print("ERROR: exact match not found")
else:
    content = content.replace(old, new, 1)
    with open('index.html', 'w') as f:
        f.write(content)
    print("SUCCESS: driver_id added to AppState.driver")
