with open('index.html', 'r') as f:
    content = f.read()

old = """function stopHomeMapWatch(){
  if(homeWatchId){navigator.geolocation.clearWatch(homeWatchId);homeWatchId=null;}
}"""

new = """function stopHomeMapWatch(){
  if(homeWatchId){navigator.geolocation.clearWatch(homeWatchId);homeWatchId=null;}
}

let _autocompleteInitDone=false;
async function initAddressAutocomplete(){
  if(_autocompleteInitDone)return;
  await loadGoogleMaps();
  const pickupInput=document.getElementById('pickupInput');
  const dropoffInput=document.getElementById('dropoffInput');
  const saOptions={componentRestrictions:{country:'za'},fields:['formatted_address','geometry']};

  if(pickupInput){
    const pAuto=new google.maps.places.Autocomplete(pickupInput,saOptions);
    pAuto.addListener('place_changed',()=>{
      const place=pAuto.getPlace();
      if(place&&place.formatted_address){
        pickupInput.value=place.formatted_address;
        AppState.pickup=place.formatted_address;
        if(place.geometry&&place.geometry.location){
          AppState.pickupLat=place.geometry.location.lat();
          AppState.pickupLng=place.geometry.location.lng();
        }
        updateAddress();
      }
    });
  }
  if(dropoffInput){
    const dAuto=new google.maps.places.Autocomplete(dropoffInput,saOptions);
    dAuto.addListener('place_changed',()=>{
      const place=dAuto.getPlace();
      if(place&&place.formatted_address){
        dropoffInput.value=place.formatted_address;
        AppState.dropoff=place.formatted_address;
        if(place.geometry&&place.geometry.location){
          AppState.dropoffLat=place.geometry.location.lat();
          AppState.dropoffLng=place.geometry.location.lng();
        }
        updateAddress();
      }
    });
  }
  _autocompleteInitDone=true;
}"""

if old not in content:
    print("ERROR: exact match not found")
else:
    content = content.replace(old, new, 1)
    with open('index.html', 'w') as f:
        f.write(content)
    print("SUCCESS: initAddressAutocomplete function added")
