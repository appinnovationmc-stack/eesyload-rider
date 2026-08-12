import sys

PATH = "index.html"

OLD = """function selV(el,vehicle){
  document.querySelectorAll('.vc').forEach(c=>c.classList.remove('sel'));
  el.classList.add('sel');
  AppState.vehiclePrice=parseFloat(vehicle.base_price)||0;
  AppState.vehiclePerKmRate=parseFloat(vehicle.per_km_rate)||0;
  AppState.vehicleName=vehicle.name;
  AppState.vehicleTypeId=vehicle.id;
  refreshPriceDisplay();
}"""

NEW = """function selVehicleState(vehicle){
  AppState.vehiclePrice=parseFloat(vehicle.base_price)||0;
  AppState.vehiclePerKmRate=parseFloat(vehicle.per_km_rate)||0;
  AppState.vehicleName=vehicle.name;
  AppState.vehicleTypeId=vehicle.id;
  refreshPriceDisplay();
}

function highlightSelectedVc(vehicleId){
  const row=document.getElementById('vcRow');
  if(!row)return;
  const cards=row.querySelectorAll('.vc');
  (_cachedVehicleTypes||[]).forEach((v,i)=>{
    if(cards[i])cards[i].classList.toggle('sel', v.id===vehicleId);
  });
}

function selV(el,vehicle){
  selVehicleState(vehicle);
  highlightSelectedVc(vehicle.id);
}"""

with open(PATH, "r", encoding="utf-8") as f:
    src = f.read()

count = src.count(OLD)
if count != 1:
    print(f"ERROR: expected exactly 1 match for OLD block, found {count}. Aborting, no changes made.")
    sys.exit(1)

src = src.replace(OLD, NEW)

with open(PATH, "w", encoding="utf-8") as f:
    f.write(src)

print("Patched selV -> selVehicleState + highlightSelectedVc + thin selV wrapper. 1 match replaced.")
