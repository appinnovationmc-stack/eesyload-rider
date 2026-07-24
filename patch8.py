import sys

BASE = "/Users/maobane/eesyload-rider"
HTML_PATH = f"{BASE}/index.html"

def apply_one(path, old, new, label):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    count = content.count(old)
    if count == 0:
        print(f"SKIP (already applied or not found): {label}")
        return
    if count > 1:
        print(f"ABORT: '{label}' matched {count} times, expected 1. No changes made to this block.")
        sys.exit(1)
    content = content.replace(old, new)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"APPLIED: {label}")

# ── 1. Track the real booking + its realtime subscription in AppState ───
old_state = """const AppState={
  pickup:'',
  dropoff:'',
  vehicleName:'Bakkie',
  vehiclePrice:110,
  addons:[], // {name, price}
  scheduled:false,
  scheduledDate:null,
  scheduledTime:null,
  isBusiness:false,
  driver:{name:'Sipho Nkosi',vehicle:'Toyota Hilux · CA 123-456',rating:4.9,loads:312},
  fare:0
};"""

new_state = """const AppState={
  pickup:'',
  dropoff:'',
  vehicleName:'Bakkie',
  vehiclePrice:110,
  addons:[], // {name, price}
  scheduled:false,
  scheduledDate:null,
  scheduledTime:null,
  isBusiness:false,
  driver:{name:'Sipho Nkosi',vehicle:'Toyota Hilux · CA 123-456',rating:4.9,loads:312},
  fare:0,
  currentBookingId:null,
  bookingSub:null
};"""

apply_one(HTML_PATH, old_state, new_state, "AppState now tracks real booking id + subscription")

# ── 2. findDriver(): actually create the booking and listen for real driver match ──
old_find = """function findDriver(){
  go('searching');
  setTimeout(()=>{
    if(document.getElementById('searching').classList.contains('on'))go('tracking');
  },3000);
}"""

new_find = """async function findDriver(){
  go('searching');
  try{
    const booking=await createBooking({
      pickup_address: AppState.pickup,
      dropoff_address: AppState.dropoff,
      vehicle_name: AppState.vehicleName,
      base_fare: AppState.vehiclePrice,
      total_fare: calcFare(),
      addons: AppState.addons,
      addons_total: AppState.addons.reduce((s,a)=>s+a.price,0)
    });
    AppState.currentBookingId=booking.id;
    if(AppState.bookingSub){sb.removeChannel(AppState.bookingSub);}
    AppState.bookingSub=subscribeToBookingUpdates(booking.id, async(updated)=>{
      if(updated.status==='accepted' && updated.driver_id){
        try{
          const driver=await getDriverProfile(updated.driver_id);
          AppState.driver={
            name: driver.full_name||'Your driver',
            vehicle: (driver.vehicle_type||'')+(driver.vehicle_plate?(' · '+driver.vehicle_plate):''),
            rating: 5.0,
            loads: 0
          };
        }catch(e){console.error('Could not load driver profile',e);}
        if(document.getElementById('searching').classList.contains('on'))go('tracking');
      }else if(updated.status==='delivered'){
        if(AppState.bookingSub){sb.removeChannel(AppState.bookingSub);AppState.bookingSub=null;}
        go('delivered');
      }else if(updated.status==='cancelled_driver'){
        if(AppState.bookingSub){sb.removeChannel(AppState.bookingSub);AppState.bookingSub=null;}
        alert('Your driver cancelled this load. Please try booking again.');
        go('booking');
      }
    });
  }catch(e){
    console.error('Could not create booking',e);
    alert('Could not request a driver: '+e.message);
    go('confirm');
  }
}

async function cancelSearch(){
  if(AppState.bookingSub){sb.removeChannel(AppState.bookingSub);AppState.bookingSub=null;}
  if(AppState.currentBookingId){
    try{await cancelBookingAsRider(AppState.currentBookingId);}catch(e){console.error('Could not cancel booking',e);}
    AppState.currentBookingId=null;
  }
  go('booking');
}"""

apply_one(HTML_PATH, old_find, new_find, "findDriver() now creates a real booking and listens for a real driver match")

# ── 3. Wire the "Cancel search" button to actually cancel, not just navigate away ──
old_cancel_btn = """    <div class="srch-cancel" onclick="go('booking')">Cancel search</div>"""
new_cancel_btn = """    <div class="srch-cancel" onclick="cancelSearch()">Cancel search</div>"""
apply_one(HTML_PATH, old_cancel_btn, new_cancel_btn, "Cancel search button now actually cancels the booking")

# ── 4. cancelLoad() (from tracking screen) also cancels the real booking ────
old_cancel_load = """function cancelLoad(){
  if(!confirm('Cancel this load? This cannot be undone.'))return;
  saveLoadToHistory('cancelled');
  go('home');
}"""

new_cancel_load = """async function cancelLoad(){
  if(!confirm('Cancel this load? This cannot be undone.'))return;
  if(AppState.bookingSub){sb.removeChannel(AppState.bookingSub);AppState.bookingSub=null;}
  if(AppState.currentBookingId){
    try{await cancelBookingAsRider(AppState.currentBookingId);}catch(e){console.error('Could not cancel booking',e);}
  }
  saveLoadToHistory('cancelled');
  go('home');
}"""

apply_one(HTML_PATH, old_cancel_load, new_cancel_load, "cancelLoad() now cancels the real booking too")

print("\nDone. Review with: git diff")
