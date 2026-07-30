with open('index.html', 'r') as f:
    content = f.read()

old = """function initBookingDefaults(){
  // sync initial state to whatever card/toggles are marked selected/on in markup
  const selVc=document.querySelector('.vc.sel');
  if(selVc){AppState.vehiclePrice=parseFloat(selVc.dataset.price)||0;AppState.vehicleName=selVc.dataset.name||AppState.vehicleName;}
  AppState.addons=[];
  document.querySelectorAll('.addon-row').forEach(row=>{
    if(row.querySelector('.tog').classList.contains('on')){
      AppState.addons.push({name:row.querySelector('.addon-n').textContent.trim(),price:parseFloat(row.dataset.price)||0});
    }
  });
  refreshPriceDisplay();
}"""

new = """function initBookingDefaults(){
  // Vehicle and addon state is now maintained directly by renderVehicleTiles(),
  // renderVcCards(), and togAddon() — no need to re-derive it from DOM attributes.
  if(!AppState.addons)AppState.addons=[];
  renderAddonRows();
  refreshPriceDisplay();
}"""

if old not in content:
    print("ERROR: exact match not found")
else:
    content = content.replace(old, new, 1)
    with open('index.html', 'w') as f:
        f.write(content)
    print("SUCCESS: initBookingDefaults simplified")
