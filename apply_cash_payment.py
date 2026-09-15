#!/usr/bin/env python3
"""Idempotent patch: finish cash payment on confirm screen for www/index.html"""
from pathlib import Path
import sys

target = Path("www/index.html")
if not target.exists():
    print("Run this from the eesyload-rider repo root")
    sys.exit(1)

html = target.read_text()

# 1. AppState
old = """const AppState={
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
new = """const AppState={
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
  bookingSub:null,
  paymentMethod:'paystack_card' // 'paystack_card' | 'cash'
};"""
if old in html:
    html = html.replace(old, new)
    print("✓ AppState.paymentMethod added")
elif "paymentMethod:'paystack_card'" in html or 'paymentMethod: "paystack_card"' in html:
    print("✓ AppState.paymentMethod already present")
else:
    print("! AppState block not matched — manual check needed")

# 2. pay-row
old = '''      <div class="pay-row" onclick="go('payments')">
        <div style="display:flex;align-items:center;gap:10px;">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none"><rect x="2" y="5" width="20" height="14" rx="3" stroke="var(--g40)" stroke-width="2"/><path d="M2 10h20" stroke="var(--g40)" stroke-width="2"/><rect x="5" y="14" width="5" height="2" rx="1" fill="var(--g60)"/></svg>
          <div><div class="pay-s">Change payment method</div></div>
        </div>
        <svg width="8" height="13" viewBox="0 0 8 14" fill="none"><path d="M1 1l6 6-6 6" stroke="var(--g80)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
      </div>'''
new = '''      <div class="pay-row" onclick="togglePaymentMethod()">
        <div style="display:flex;align-items:center;gap:10px;">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" id="cfPayIcon"><rect x="2" y="5" width="20" height="14" rx="3" stroke="var(--g40)" stroke-width="2"/><path d="M2 10h20" stroke="var(--g40)" stroke-width="2"/><rect x="5" y="14" width="5" height="2" rx="1" fill="var(--g60)"/></svg>
          <div>
            <div class="pay-l" id="cfPayLabel">Card</div>
            <div class="pay-s" id="cfPaySub">Tap to switch to cash</div>
          </div>
        </div>
        <svg width="8" height="13" viewBox="0 0 8 14" fill="none"><path d="M1 1l6 6-6 6" stroke="var(--g80)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
      </div>'''
if old in html:
    html = html.replace(old, new)
    print("✓ Confirm pay-row now toggles cash/card")
elif 'id="cfPayLabel"' in html:
    print("✓ Confirm pay-row already updated")
else:
    print("! pay-row not matched")

# 3. renderConfirmScreen
old = """function renderConfirmScreen(){
  const set=(id,val)=>{const el=document.getElementById(id);if(el)el.textContent=val;};
  set('cfVehicle',AppState.vehicleName);
  set('cfPickup',AppState.pickup||'—');
  set('cfDropoff',AppState.dropoff||'—');
  set('cfAddons',AppState.addons.length?AppState.addons.map(a=>a.name).join(', '):'None');
  set('cfTotal','R'+calcFare());

  const payBtn = document.querySelector('[onclick="payAndFindDriver()"]');
  if(payBtn){ payBtn.disabled = false; payBtn.textContent = 'Find my driver'; }
}"""
new = """function renderConfirmScreen(){
  const set=(id,val)=>{const el=document.getElementById(id);if(el)el.textContent=val;};
  set('cfVehicle',AppState.vehicleName);
  set('cfPickup',AppState.pickup||'—');
  set('cfDropoff',AppState.dropoff||'—');
  set('cfAddons',AppState.addons.length?AppState.addons.map(a=>a.name).join(', '):'None');
  set('cfTotal','R'+calcFare());

  // Payment method display on confirm
  const isCash = AppState.paymentMethod === 'cash';
  set('cfPayLabel', isCash ? 'Cash on delivery' : 'Card');
  set('cfPaySub', isCash ? 'Tap to switch to card' : 'Tap to switch to cash');
  const icon = document.getElementById('cfPayIcon');
  if(icon){
    if(isCash){
      icon.innerHTML = '<circle cx="12" cy="12" r="9" stroke="var(--g40)" stroke-width="2"/><path d="M12 7v10M9 10h6M9 14h6" stroke="var(--g40)" stroke-width="2" stroke-linecap="round"/>';
    }else{
      icon.innerHTML = '<rect x="2" y="5" width="20" height="14" rx="3" stroke="var(--g40)" stroke-width="2"/><path d="M2 10h20" stroke="var(--g40)" stroke-width="2"/><rect x="5" y="14" width="5" height="2" rx="1" fill="var(--g60)"/>';
    }
  }

  const payBtn = document.querySelector('[onclick="payAndFindDriver()"]');
  if(payBtn){ payBtn.disabled = false; payBtn.textContent = isCash ? 'Request driver (pay cash)' : 'Find my driver'; }
}

function togglePaymentMethod(){
  AppState.paymentMethod = AppState.paymentMethod === 'cash' ? 'paystack_card' : 'cash';
  renderConfirmScreen();
}"""
if old in html:
    html = html.replace(old, new)
    print("✓ renderConfirmScreen + togglePaymentMethod added")
elif "function togglePaymentMethod" in html:
    print("✓ toggle already present")
else:
    print("! renderConfirmScreen not matched")

# 4. payAndFindDriver — insert cash branch at the top
if "const isCash = AppState.paymentMethod === 'cash';" in html:
    print("✓ cash branch already in payAndFindDriver")
else:
    marker = """async function payAndFindDriver(){
  const amountZAR = calcFare();
  const user = await sbGetCurrentUser();
  if(!user){ alert('Please sign in again.'); return; }

  const btn = document.querySelector('[onclick="payAndFindDriver()"]');
  if(btn){ btn.disabled = true; btn.textContent = 'Opening payment...'; }

  const methods = await getEnabledPaymentMethods();"""
    insert = """async function payAndFindDriver(){
  const user = await sbGetCurrentUser();
  if(!user){ alert('Please sign in again.'); return; }

  const btn = document.querySelector('[onclick="payAndFindDriver()"]');
  const isCash = AppState.paymentMethod === 'cash';

  // ── Cash path: skip Paystack, create booking immediately ──
  if(isCash){
    if(btn){ btn.disabled = true; btn.textContent = 'Requesting driver...'; }
    window._pendingPaystackRef = null;
    try{
      await findDriver();
    }catch(e){
      if(btn){ btn.disabled = false; btn.textContent = 'Request driver (pay cash)'; }
    }
    return;
  }

  // ── Card / Paystack path ──
  const amountZAR = calcFare();
  if(btn){ btn.disabled = true; btn.textContent = 'Opening payment...'; }

  const methods = await getEnabledPaymentMethods();"""
    if marker in html:
        html = html.replace(marker, insert)
        print("✓ cash branch injected into payAndFindDriver")
    else:
        print("! payAndFindDriver marker not found — open the file and add the cash if(isCash) block manually")

# 5. createBooking call
old = """      paystack_reference: window._pendingPaystackRef || null
    });"""
new = """      paystack_reference: window._pendingPaystackRef || null,
      payment_method: AppState.paymentMethod || 'paystack_card'
    });"""
if old in html and "payment_method: AppState.paymentMethod" not in html:
    html = html.replace(old, new)
    print("✓ payment_method added to createBooking call")
elif "payment_method: AppState.paymentMethod" in html:
    print("✓ payment_method already in createBooking call")
else:
    print("! createBooking call not matched")

target.write_text(html)
print("\nDone. Review with: git diff www/index.html")
print("Then commit & push.")
