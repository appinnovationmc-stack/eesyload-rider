with open('index.html', 'r') as f:
    content = f.read()

old = """function calcFare(){
  return AppState.vehiclePrice + AppState.addons.reduce((sum,a)=>sum+a.price,0);
}"""

new = """function calcFare(){
  const distanceCost=(AppState.vehiclePerKmRate||0)*(AppState.routeDistanceKm||0);
  return AppState.vehiclePrice + distanceCost + AppState.addons.reduce((sum,a)=>sum+a.price,0);
}

async function calculateRouteDistance(){
  if(!AppState.pickup||!AppState.dropoff){AppState.routeDistanceKm=0;return;}
  await loadGoogleMaps();
  return new Promise((resolve)=>{
    const svc=new google.maps.DirectionsService();
    svc.route({origin:AppState.pickup,destination:AppState.dropoff,travelMode:google.maps.TravelMode.DRIVING},(res,status)=>{
      if(status==='OK'&&res.routes[0]&&res.routes[0].legs[0]){
        AppState.routeDistanceKm=res.routes[0].legs[0].distance.value/1000;
      }else{
        console.error('Could not calculate route distance, status:',status);
        AppState.routeDistanceKm=0;
      }
      resolve();
    });
  });
}"""

if old not in content:
    print("ERROR: exact match not found")
else:
    content = content.replace(old, new, 1)
    with open('index.html', 'w') as f:
        f.write(content)
    print("SUCCESS: calcFare updated with distance pricing, calculateRouteDistance added")
