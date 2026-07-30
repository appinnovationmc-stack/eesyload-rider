with open('index.html', 'r') as f:
    content = f.read()

old = """function selV(el){
  document.querySelectorAll('.vc').forEach(c=>c.classList.remove('sel'));
  el.classList.add('sel');
  AppState.vehiclePrice=parseFloat(el.dataset.price)||0;
  AppState.vehicleName=el.dataset.name||el.querySelector('.vc-n').textContent;
  refreshPriceDisplay();
}"""

new = """const _vcIllustrationMap={
  'Moto':'<svg width="52" height="28" viewBox="0 0 52 28" fill="none"><circle cx="10" cy="22" r="5" stroke="white" stroke-width="1.8"/><circle cx="36" cy="22" r="5" stroke="white" stroke-width="1.8"/><path d="M4 22V14L10 4h8l5 8" stroke="white" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/><path d="M17 4h12a2 2 0 012 2v9H4" stroke="white" stroke-width="1.8" stroke-linecap="round"/><path d="M31 15h14l-3-9H31v9z" stroke="white" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>',
  'Bakkie':'<svg width="58" height="28" viewBox="0 0 62 28" fill="none"><rect x="16" y="3" width="34" height="17" rx="2.5" stroke="white" stroke-width="1.8"/><path d="M3 14h13l5-11h7" stroke="white" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/><path d="M2 14v7h58v-7" stroke="white" stroke-width="1.8" stroke-linecap="round"/><circle cx="13" cy="24" r="4" stroke="white" stroke-width="1.8"/><circle cx="47" cy="24" r="4" stroke="white" stroke-width="1.8"/></svg>',
  'Van':'<svg width="54" height="28" viewBox="0 0 56 28" fill="none"><path d="M2 20V11c0-2 2-4 3.5-5L24 4h26a3 3 0 013 3v13" stroke="white" stroke-width="1.8" stroke-linecap="round"/><path d="M2 20h52" stroke="white" stroke-width="1.8" stroke-linecap="round"/><rect x="6" y="7" width="9" height="7" rx="1.5" stroke="white" stroke-width="1.5"/><rect x="18" y="7" width="9" height="7" rx="1.5" stroke="white" stroke-width="1.5"/><circle cx="12" cy="24" r="4" stroke="white" stroke-width="1.8"/><circle cx="42" cy="24" r="4" stroke="white" stroke-width="1.8"/></svg>',
  '4-Ton':'<svg width="58" height="28" viewBox="0 0 62 28" fill="none"><rect x="2" y="4" width="36" height="17" rx="2" stroke="white" stroke-width="1.8"/><path d="M38 10h16l5 8v4H38V10z" stroke="white" stroke-width="1.8" stroke-linejoin="round"/><circle cx="12" cy="24" r="4" stroke="white" stroke-width="1.8"/><circle cx="28" cy="24" r="4" stroke="white" stroke-width="1.8"/><circle cx="50" cy="24" r="4" stroke="white" stroke-width="1.8"/><rect x="6" y="7" width="11" height="8" rx="1.5" stroke="white" stroke-width="1.5"/></svg>',
  '8-Ton':'<svg width="58" height="28" viewBox="0 0 62 28" fill="none"><rect x="2" y="2" width="58" height="20" rx="2" stroke="white" stroke-width="1.8"/><rect x="8" y="6" width="14" height="10" rx="1" stroke="white" stroke-width="1.5"/><rect x="26" y="6" width="14" height="10" rx="1" stroke="white" stroke-width="1.5"/><rect x="44" y="6" width="12" height="10" rx="1" stroke="white" stroke-width="1.5"/><circle cx="10" cy="25" r="3" stroke="white" stroke-width="1.8"/><circle cx="26" cy="25" r="3" stroke="white" stroke-width="1.8"/><circle cx="42" cy="25" r="3" stroke="white" stroke-width="1.8"/><circle cx="54" cy="25" r="3" stroke="white" stroke-width="1.8"/></svg>',
  '_default':'<svg width="58" height="28" viewBox="0 0 62 28" fill="none"><rect x="2" y="4" width="32" height="16" rx="2" stroke="white" stroke-width="1.8"/><path d="M34 9h12l5 8v4H34V9z" stroke="white" stroke-width="1.8" stroke-linejoin="round"/><circle cx="11" cy="24" r="4" stroke="white" stroke-width="1.8"/><circle cx="26" cy="24" r="4" stroke="white" stroke-width="1.8"/><circle cx="43" cy="24" r="4" stroke="white" stroke-width="1.8"/></svg>'
};

async function renderVcCards(){
  const row=document.getElementById('vcRow');
  if(!row)return;
  let vehicles=_cachedVehicleTypes;
  if(!vehicles||!vehicles.length){
    try{vehicles=await getVehicleTypes();_cachedVehicleTypes=vehicles;}catch(e){console.error('Could not load vehicle types',e);return;}
  }
  row.innerHTML='';
  vehicles.forEach((v)=>{
    const illustration=_vcIllustrationMap[v.name]||_vcIllustrationMap['_default'];
    const isSelected=AppState.vehicleTypeId?v.id===AppState.vehicleTypeId:v.name===AppState.vehicleName;
    const card=document.createElement('div');
    card.className='vc'+(isSelected?' sel':'');
    card.onclick=function(){selV(this,v);};
    card.innerHTML=
      (v.name==='Bakkie'?'<div class="vcb">POPULAR</div>':'')+
      '<div class="vc-ill">'+illustration+'</div>'+
      '<div class="vc-n">'+v.name+'</div>'+
      '<div class="vc-c">'+(v.capacity_label||'')+'</div>'+
      '<div class="vc-p">From R'+Math.round(v.base_price)+'</div>';
    row.appendChild(card);
  });
}

function selV(el,vehicle){
  document.querySelectorAll('.vc').forEach(c=>c.classList.remove('sel'));
  el.classList.add('sel');
  AppState.vehiclePrice=parseFloat(vehicle.base_price)||0;
  AppState.vehiclePerKmRate=parseFloat(vehicle.per_km_rate)||0;
  AppState.vehicleName=vehicle.name;
  AppState.vehicleTypeId=vehicle.id;
  refreshPriceDisplay();
}"""

if old not in content:
    print("ERROR: exact match not found")
else:
    content = content.replace(old, new, 1)
    with open('index.html', 'w') as f:
        f.write(content)
    print("SUCCESS: dynamic vc card rendering added")
