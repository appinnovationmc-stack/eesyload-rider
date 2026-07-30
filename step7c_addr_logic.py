with open('index.html', 'r') as f:
    content = f.read()

old = """function stopHomeMapWatch(){
  if(homeWatchId){navigator.geolocation.clearWatch(homeWatchId);homeWatchId=null;}
}"""

new = """function stopHomeMapWatch(){
  if(homeWatchId){navigator.geolocation.clearWatch(homeWatchId);homeWatchId=null;}
}

let _cachedSavedAddresses=[];
async function renderSavedAddressesUI(){
  try{
    _cachedSavedAddresses=await getSavedAddresses();
  }catch(e){
    console.error('Could not load saved addresses',e);
    return;
  }
  const home=_cachedSavedAddresses.find(a=>a.label==='Home');
  const work=_cachedSavedAddresses.find(a=>a.label==='Work');
  const homeSub=document.getElementById('savedAddrHomeSub');
  const workSub=document.getElementById('savedAddrWorkSub');
  if(homeSub)homeSub.textContent=home?home.formatted_address:'Tap to add';
  if(workSub)workSub.textContent=work?work.formatted_address:'Tap to add';
}

function _geocodeAddressText(addressText){
  return new Promise(async(resolve,reject)=>{
    await loadGoogleMaps();
    const geocoder=new google.maps.Geocoder();
    geocoder.geocode({address:addressText},(results,status)=>{
      if(status==='OK'&&results&&results[0]){
        resolve({
          formatted_address:results[0].formatted_address,
          lat:results[0].geometry.location.lat(),
          lng:results[0].geometry.location.lng()
        });
      }else{
        reject(new Error('Could not find that address'));
      }
    });
  });
}

async function useOrAddSavedAddress(label){
  const existing=_cachedSavedAddresses.find(a=>a.label===label);
  if(existing){
    AppState.pickup=existing.formatted_address;
    AppState.pickupLat=existing.lat;
    AppState.pickupLng=existing.lng;
    go('booking');
    setTimeout(()=>{
      const pickupInput=document.getElementById('pickupInput');
      if(pickupInput)pickupInput.value=existing.formatted_address;
    },50);
    return;
  }
  const typed=prompt('Enter your '+label+' address:');
  if(!typed)return;
  try{
    const geo=await _geocodeAddressText(typed);
    await saveAddress(label,geo.formatted_address,geo.lat,geo.lng);
    await renderSavedAddressesUI();
    AppState.pickup=geo.formatted_address;
    AppState.pickupLat=geo.lat;
    AppState.pickupLng=geo.lng;
    go('booking');
    setTimeout(()=>{
      const pickupInput=document.getElementById('pickupInput');
      if(pickupInput)pickupInput.value=geo.formatted_address;
    },50);
  }catch(e){
    alert('Could not save that address. Please check it and try again.');
  }
}

async function addCustomSavedAddress(){
  const label=prompt('Name this address (e.g. "Gym", "Mom\\'s house"):');
  if(!label)return;
  const typed=prompt('Enter the address:');
  if(!typed)return;
  try{
    const geo=await _geocodeAddressText(typed);
    await saveAddress(label,geo.formatted_address,geo.lat,geo.lng);
    await renderSavedAddressesUI();
    alert('Address saved.');
  }catch(e){
    alert('Could not save that address. Please check it and try again.');
  }
}"""

if old not in content:
    print("ERROR: exact match not found")
else:
    content = content.replace(old, new, 1)
    with open('index.html', 'w') as f:
        f.write(content)
    print("SUCCESS: saved address UI functions added")
