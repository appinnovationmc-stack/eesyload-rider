with open('index.html', 'r') as f:
    content = f.read()

old = """function calcFare(){
  const distanceCost=(AppState.vehiclePerKmRate||0)*(AppState.routeDistanceKm||0);
  return AppState.vehiclePrice + distanceCost + AppState.addons.reduce((sum,a)=>sum+a.price,0);
}"""

new = """function calcFare(){
  const distanceCost=(AppState.vehiclePerKmRate||0)*(AppState.routeDistanceKm||0);
  const total=AppState.vehiclePrice + distanceCost + AppState.addons.reduce((sum,a)=>sum+a.price,0);
  return Math.round(total);
}"""

if old not in content:
    print("ERROR: exact match not found")
else:
    content = content.replace(old, new, 1)
    with open('index.html', 'w') as f:
        f.write(content)
    print("SUCCESS: calcFare now rounds to whole Rand")
