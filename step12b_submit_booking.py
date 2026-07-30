with open('index.html', 'r') as f:
    content = f.read()

old = """function submitBooking(){
  if(!AppState.pickup.trim()||!AppState.dropoff.trim()){
    const p=document.getElementById('pickupInput'),d=document.getElementById('dropoffInput');
    if(!AppState.pickup.trim()&&p){p.style.borderColor='#FF3B30';p.focus();}
    if(!AppState.dropoff.trim()&&d){d.style.borderColor='#FF3B30';}
    setTimeout(()=>{if(p)p.style.borderColor='';if(d)d.style.borderColor='';},1200);
    return;
  }
  refreshPriceDisplay();
  go('confirm');
}"""

new = """async function submitBooking(){
  if(!AppState.pickup.trim()||!AppState.dropoff.trim()){
    const p=document.getElementById('pickupInput'),d=document.getElementById('dropoffInput');
    if(!AppState.pickup.trim()&&p){p.style.borderColor='#FF3B30';p.focus();}
    if(!AppState.dropoff.trim()&&d){d.style.borderColor='#FF3B30';}
    setTimeout(()=>{if(p)p.style.borderColor='';if(d)d.style.borderColor='';},1200);
    return;
  }
  const btn=document.querySelector('[onclick="submitBooking()"]');
  if(btn){btn.disabled=true;btn.textContent='Calculating route…';}
  try{
    await calculateRouteDistance();
  }catch(e){
    console.error('Route calculation failed',e);
    AppState.routeDistanceKm=0;
  }
  if(btn){btn.disabled=false;btn.innerHTML='Confirm load <svg width="17" height="17" viewBox="0 0 24 24" fill="none"><path d="M5 12h14M13 6l6 6-6 6" stroke="black" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/></svg>';}
  refreshPriceDisplay();
  go('confirm');
}"""

if old not in content:
    print("ERROR: exact match not found")
else:
    content = content.replace(old, new, 1)
    with open('index.html', 'w') as f:
        f.write(content)
    print("SUCCESS: submitBooking now calculates real route distance")
