with open('index.html', 'r') as f:
    content = f.read()

old = """const vehicleTileMap={Bakkie:110,Truck:320,Van:185,Moto:65,Helpers:110};
function selTile(el){
  document.querySelectorAll('.tile').forEach(t=>t.classList.remove('on'));
  el.classList.add('on');
  const name=el.querySelector('.tl').textContent.trim();
  if(vehicleTileMap[name]){
    AppState.vehicleName=name;
    AppState.vehiclePrice=vehicleTileMap[name];
  }
}"""

new = """const _vehicleIconMap={
  'Bakkie':'<svg width="40" height="24" viewBox="0 0 50 28" fill="none"><rect x="14" y="3" width="32" height="16" rx="2.5" stroke="white" stroke-width="1.8"/><path d="M3 13h11l5-10h6" stroke="white" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/><path d="M2 13v8h47v-8" stroke="white" stroke-width="1.8" stroke-linecap="round"/><circle cx="12" cy="24" r="4" stroke="white" stroke-width="1.8"/><circle cx="39" cy="24" r="4" stroke="white" stroke-width="1.8"/></svg>',
  'Van':'<svg width="40" height="24" viewBox="0 0 50 28" fill="none"><path d="M2 20V11c0-2 1.5-4 3-4L22 4h22a3 3 0 013 3v13" stroke="white" stroke-width="1.8" stroke-linecap="round"/><path d="M2 20h46" stroke="white" stroke-width="1.8" stroke-linecap="round"/><rect x="6" y="7" width="9" height="7" rx="1.5" stroke="white" stroke-width="1.5"/><rect x="18" y="7" width="9" height="7" rx="1.5" stroke="white" stroke-width="1.5"/><circle cx="11" cy="24" r="4" stroke="white" stroke-width="1.8"/><circle cx="37" cy="24" r="4" stroke="white" stroke-width="1.8"/></svg>',
  'Moto':'<svg width="36" height="24" viewBox="0 0 42 26" fill="none"><circle cx="9" cy="20" r="5.5" stroke="white" stroke-width="1.8"/><circle cx="33" cy="20" r="5.5" stroke="white" stroke-width="1.8"/><path d="M14.5 20H27.5M21 20V9" stroke="white" stroke-width="1.8" stroke-linecap="round"/><path d="M15 9h12l4 6H11l4-6z" stroke="white" stroke-width="1.8" stroke-linejoin="round"/><path d="M21 9V4l5-3" stroke="white" stroke-width="1.8" stroke-linecap="round"/></svg>',
  '_default_truck':'<svg width="40" height="24" viewBox="0 0 52 28" fill="none"><rect x="2" y="4" width="32" height="16" rx="2" stroke="white" stroke-width="1.8"/><path d="M34 9h12l5 8v4H34V9z" stroke="white" stroke-width="1.8" stroke-linejoin="round"/><circle cx="11" cy="24" r="4" stroke="white" stroke-width="1.8"/><circle cx="26" cy="24" r="4" stroke="white" stroke-width="1.8"/><circle cx="43" cy="24" r="4" stroke="white" stroke-width="1.8"/></svg>'
};

let _cachedVehicleTypes=[];
async function renderVehicleTiles(){
  const row=document.getElementById('tileRow');
  if(!row)return;
  try{
    _cachedVehicleTypes=await getVehicleTypes();
  }catch(e){
    console.error('Could not load vehicle types',e);
    return;
  }
  row.innerHTML='';
  _cachedVehicleTypes.forEach((v,i)=>{
    const icon=_vehicleIconMap[v.name]||_vehicleIconMap['_default_truck'];
    const tile=document.createElement('div');
    tile.className='tile'+(i===0?' on':'');
    tile.onclick=function(){selTile(this,v);};
    tile.innerHTML='<div class="ti">'+icon+'</div><span class="tl">'+v.name+'</span>';
    row.appendChild(tile);
  });
  if(_cachedVehicleTypes.length){
    const first=_cachedVehicleTypes[0];
    AppState.vehicleName=first.name;
    AppState.vehiclePrice=parseFloat(first.base_price)||0;
    AppState.vehiclePerKmRate=parseFloat(first.per_km_rate)||0;
    AppState.vehicleTypeId=first.id;
  }
}

function selTile(el,vehicle){
  document.querySelectorAll('.tile').forEach(t=>t.classList.remove('on'));
  el.classList.add('on');
  AppState.vehicleName=vehicle.name;
  AppState.vehiclePrice=parseFloat(vehicle.base_price)||0;
  AppState.vehiclePerKmRate=parseFloat(vehicle.per_km_rate)||0;
  AppState.vehicleTypeId=vehicle.id;
  refreshPriceDisplay();
}"""

if old not in content:
    print("ERROR: exact match not found")
else:
    content = content.replace(old, new, 1)
    with open('index.html', 'w') as f:
        f.write(content)
    print("SUCCESS: dynamic vehicle tile rendering added")
