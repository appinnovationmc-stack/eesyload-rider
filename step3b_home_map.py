with open('index.html', 'r') as f:
    content = f.read()

old = """let _homeRaf=null;
function go(id){
  document.querySelectorAll('.scr').forEach(s=>s.classList.remove('on'));
  document.getElementById(id).classList.add('on');
  if(id==='home'){if(_homeRaf)cancelAnimationFrame(_homeRaf);_animateHome();}else{if(_homeRaf){cancelAnimationFrame(_homeRaf);_homeRaf=null;}}"""

new = """let _homeRaf=null;
let _mapsReadyPromise=null;
function loadGoogleMaps(){
  if(_mapsReadyPromise)return _mapsReadyPromise;
  _mapsReadyPromise=new Promise((resolve)=>{
    if(window.google&&window.google.maps){resolve();return;}
    const s=document.createElement('script');
    s.src='https://maps.googleapis.com/maps/api/js?key=AIzaSyBAUx4OpJivUYKzeh0Ol7zFjIlHY4czQQM&v=weekly';
    s.async=true;
    s.onload=()=>resolve();
    document.head.appendChild(s);
  });
  return _mapsReadyPromise;
}
let homeMap=null,homeMarker=null,homeWatchId=null;
async function initHomeMap(){
  await loadGoogleMaps();
  const el=document.getElementById('hmap');
  if(!el)return;
  const fallback={lat:-25.7479,lng:28.2293}; // Pretoria fallback
  if(!homeMap){
    homeMap=new google.maps.Map(el,{center:fallback,zoom:15,disableDefaultUI:true,zoomControl:true});
    homeMarker=new google.maps.Marker({map:homeMap,position:fallback});
  }
  if(!navigator.geolocation)return;
  navigator.geolocation.getCurrentPosition(pos=>{
    const p={lat:pos.coords.latitude,lng:pos.coords.longitude};
    homeMap.setCenter(p);homeMarker.setPosition(p);
  },()=>{});
  if(homeWatchId)navigator.geolocation.clearWatch(homeWatchId);
  homeWatchId=navigator.geolocation.watchPosition(pos=>{
    const p={lat:pos.coords.latitude,lng:pos.coords.longitude};
    homeMap.setCenter(p);homeMarker.setPosition(p);
  },()=>{},{enableHighAccuracy:true,maximumAge:5000});
}
function stopHomeMapWatch(){
  if(homeWatchId){navigator.geolocation.clearWatch(homeWatchId);homeWatchId=null;}
}
function go(id){
  document.querySelectorAll('.scr').forEach(s=>s.classList.remove('on'));
  document.getElementById(id).classList.add('on');
  if(id==='home'){initHomeMap();}else{stopHomeMapWatch();}"""

if old not in content:
    print("ERROR: exact match not found")
else:
    content = content.replace(old, new, 1)
    with open('index.html', 'w') as f:
        f.write(content)
    print("SUCCESS: loadGoogleMaps, initHomeMap added and wired into go()")
