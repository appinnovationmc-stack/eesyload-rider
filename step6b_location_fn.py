with open('index.html', 'r') as f:
    content = f.read()

old = """function stopHomeMapWatch(){
  if(homeWatchId){navigator.geolocation.clearWatch(homeWatchId);homeWatchId=null;}
}"""

new = """function stopHomeMapWatch(){
  if(homeWatchId){navigator.geolocation.clearWatch(homeWatchId);homeWatchId=null;}
}

async function useCurrentLocationForPickup(){
  const labelEl=document.getElementById('useCurrentLocationLabel');
  if(!navigator.geolocation){
    alert('Location services are not available on this device.');
    return;
  }
  if(labelEl)labelEl.textContent='Detecting your location…';
  navigator.geolocation.getCurrentPosition(async(pos)=>{
    const p={lat:pos.coords.latitude,lng:pos.coords.longitude};
    try{
      await loadGoogleMaps();
      const geocoder=new google.maps.Geocoder();
      geocoder.geocode({location:p},(results,status)=>{
        if(status==='OK'&&results&&results[0]){
          const address=results[0].formatted_address;
          AppState.pickup=address;
          AppState.pickupLat=p.lat;
          AppState.pickupLng=p.lng;
          if(labelEl)labelEl.textContent='Use current location';
          go('booking');
          setTimeout(()=>{
            const pickupInput=document.getElementById('pickupInput');
            if(pickupInput)pickupInput.value=address;
          },50);
        }else{
          if(labelEl)labelEl.textContent='Use current location';
          alert('Could not detect your address. Please type it manually.');
        }
      });
    }catch(e){
      if(labelEl)labelEl.textContent='Use current location';
      alert('Could not detect your location.');
    }
  },()=>{
    if(labelEl)labelEl.textContent='Use current location';
    alert('Location access was denied. Please enable location permissions or type your address manually.');
  },{enableHighAccuracy:true,timeout:10000});
}"""

if old not in content:
    print("ERROR: exact match not found")
else:
    content = content.replace(old, new, 1)
    with open('index.html', 'w') as f:
        f.write(content)
    print("SUCCESS: useCurrentLocationForPickup function added")
