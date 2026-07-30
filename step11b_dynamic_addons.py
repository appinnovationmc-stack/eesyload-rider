with open('index.html', 'r') as f:
    content = f.read()

old = """function togAddon(row){
  const tog=row.querySelector('.tog');
  tog.classList.toggle('on');
  const name=row.querySelector('.addon-n').textContent.trim();
  const price=parseFloat(row.dataset.price)||0;
  if(tog.classList.contains('on')){
    if(!AppState.addons.find(a=>a.name===name))AppState.addons.push({name,price});
  }else{
    AppState.addons=AppState.addons.filter(a=>a.name!==name);
  }
  refreshPriceDisplay();
}"""

new = """const _addonIconMap={
  'helpers':'<svg width="18" height="18" viewBox="0 0 24 24" fill="none"><circle cx="9" cy="7" r="3" stroke="white" stroke-width="2"/><path d="M3 21c0-3.3 2.7-6 6-6s6 2.7 6 6" stroke="white" stroke-width="2" stroke-linecap="round"/><circle cx="17" cy="7" r="3" stroke="white" stroke-width="2"/><path d="M14 21c0-2 1.5-5 6-5" stroke="white" stroke-width="2" stroke-linecap="round"/></svg>',
  'blankets':'<svg width="18" height="18" viewBox="0 0 24 24" fill="none"><path d="M21 8H3a1 1 0 00-1 1v11a1 1 0 001 1h18a1 1 0 001-1V9a1 1 0 00-1-1z" stroke="white" stroke-width="2"/><path d="M9 8V5a1 1 0 011-1h4a1 1 0 011 1v3" stroke="white" stroke-width="2"/></svg>',
  'insurance':'<svg width="18" height="18" viewBox="0 0 24 24" fill="none"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>',
  'priority':'<svg width="18" height="18" viewBox="0 0 24 24" fill="none"><path d="M4 15s1-1 4-1 5 2 8 2 4-1 4-1V3s-1 1-4 1-5-2-8-2-4 1-4 1z" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><line x1="4" y1="22" x2="4" y2="15" stroke="white" stroke-width="2" stroke-linecap="round"/></svg>',
  '_default':'<svg width="18" height="18" viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="9" stroke="white" stroke-width="2"/></svg>'
};

async function renderAddonRows(){
  const container=document.getElementById('addonRow');
  if(!container)return;
  let addons=[];
  try{addons=await getServiceAddons();}catch(e){console.error('Could not load add-ons',e);return;}
  container.innerHTML='';
  addons.forEach(a=>{
    const icon=_addonIconMap[a.icon_key]||_addonIconMap['_default'];
    const isOn=AppState.addons.some(sel=>sel.id===a.id);
    const row=document.createElement('div');
    row.className='addon-row';
    row.onclick=function(){togAddon(row,a);};
    row.innerHTML=
      '<div class="addon-l"><div class="addon-ic">'+icon+'</div><div><div class="addon-n">'+a.name+'</div><div class="addon-s">+R'+Math.round(a.price)+(a.description?(' · '+a.description):'')+'</div></div></div>'+
      '<div class="tog'+(isOn?' on':'')+'"><div class="togt"></div></div>';
    container.appendChild(row);
  });
}

function togAddon(row,addon){
  const tog=row.querySelector('.tog');
  tog.classList.toggle('on');
  if(tog.classList.contains('on')){
    if(!AppState.addons.find(a=>a.id===addon.id))AppState.addons.push({id:addon.id,name:addon.name,price:parseFloat(addon.price)||0});
  }else{
    AppState.addons=AppState.addons.filter(a=>a.id!==addon.id);
  }
  refreshPriceDisplay();
}"""

if old not in content:
    print("ERROR: exact match not found")
else:
    content = content.replace(old, new, 1)
    with open('index.html', 'w') as f:
        f.write(content)
    print("SUCCESS: dynamic addon rendering added")
