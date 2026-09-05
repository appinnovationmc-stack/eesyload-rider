#!/usr/bin/env python3
from pathlib import Path
root = Path(__file__).resolve().parents[1]
p = root / "www" / "index.html"
t = p.read_text(encoding="utf-8")

def sub(old, new, label):
    global t
    if old in t:
        t = t.replace(old, new, 1)
        print("OK  ", label)
    else:
        print("SKIP", label)

sub("function submitBooking(){", "async function submitBooking(){", "submitBooking is async")

sub(
"function markDelivered(){\n  saveLoadToHistory('completed');\n  go('delivered');\n}",
"""async function markDelivered(){
  const id = (typeof AppState!=='undefined' && (AppState.currentBookingId||AppState.activeBookingId|| (AppState.currentBooking&&AppState.currentBooking.id)));
  if(!id){alert('No active booking to complete.');return;}
  try{
    if(typeof updateBookingStatus==='function'){
      await updateBookingStatus(id,'delivered');
    }else{
      const {error}=await sb.from('bookings').update({status:'delivered',delivered_at:new Date().toISOString()}).eq('id',id).eq('rider_id',(await sbGetCurrentUser()).id);
      if(error) throw error;
    }
  }catch(e){
    alert(e.message||'Could not complete booking');
    return;
  }
  saveLoadToHistory('completed');
  go('delivered');
}""",
"deliver writes database status",
)

if "glass.css" not in t:
    t = t.replace("</head>", '<link rel="stylesheet" href="glass.css">\n</head>')
    print("OK   glass.css linked")
else:
    print("OK   glass.css already linked")

p.write_text(t, encoding="utf-8")
print("done", p.stat().st_size)
