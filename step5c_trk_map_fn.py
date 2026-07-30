with open('index.html', 'r') as f:
    content = f.read()

old = """function stopHomeMapWatch(){
  if(homeWatchId){navigator.geolocation.clearWatch(homeWatchId);homeWatchId=null;}
}"""

new = """function stopHomeMapWatch(){
  if(homeWatchId){navigator.geolocation.clearWatch(homeWatchId);homeWatchId=null;}
}

let trkMap=null,trkDriverMarker=null,trkDirRenderer=null,trkLocationSub=null;
async function initTrackingMap(){
  await loadGoogleMaps();
  const el=document.getElementById('trkmap');
  if(!el||!AppState.driver||!AppState.driver.id)return;
  const fallback={lat:-25.7479,lng:28.2293};
  if(!trkMap){
    trkMap=new google.maps.Map(el,{center:fallback,zoom:14,disableDefaultUI:true});
    trkDriverMarker=new google.maps.Marker({map:trkMap,position:fallback});
    trkDirRenderer=new google.maps.DirectionsRenderer({map:trkMap,suppressMarkers:true,polylineOptions:{strokeColor:'#BB2235',strokeWeight:5}});
  }

  function routeAndUpdateEta(driverPos){
    const dest=AppState.pickup;
    if(!dest)return;
    const svc=new google.maps.DirectionsService();
    svc.route({origin:driverPos,destination:dest,travelMode:google.maps.TravelMode.DRIVING},(res,status)=>{
      if(status==='OK'){
        trkDirRenderer.setDirections(res);
        const leg=res.routes[0].legs[0];
        const etaEl=document.getElementById('trkEtaText');
        if(etaEl)etaEl.textContent=leg.duration.text;
        AppState.lastKnownEtaText=leg.duration.text;
      }
    });
  }

  // Initial fetch — show last known position immediately, don't wait for a live update
  try{
    const initial=await getDriverLocation(AppState.driver.id);
    if(initial){
      const p={lat:initial.lat,lng:initial.lng};
      trkMap.setCenter(p);trkDriverMarker.setPosition(p);
      routeAndUpdateEta(p);
    }
  }catch(e){console.error('Could not fetch initial driver location',e);}

  // Live updates as the driver moves
  if(trkLocationSub){sb.removeChannel(trkLocationSub);}
  trkLocationSub=subscribeToDriverLocation(AppState.driver.id, (loc)=>{
    const p={lat:loc.lat,lng:loc.lng};
    trkMap.setCenter(p);trkDriverMarker.setPosition(p);
    routeAndUpdateEta(p);
  });
}
function stopTrackingMap(){
  if(trkLocationSub){sb.removeChannel(trkLocationSub);trkLocationSub=null;}
}"""

if old not in content:
    print("ERROR: exact match not found")
else:
    content = content.replace(old, new, 1)
    with open('index.html', 'w') as f:
        f.write(content)
    print("SUCCESS: initTrackingMap added")
