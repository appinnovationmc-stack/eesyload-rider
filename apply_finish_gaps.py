#!/usr/bin/env python3
"""Restore user-supabase-integration.js (if broken) and wire schedule/ratings/business."""
from pathlib import Path
import sys
import urllib.request

ROOT = Path(__file__).resolve().parent
JS = ROOT / "www" / "user-supabase-integration.js"
HTML = ROOT / "www" / "index.html"

GOOD_JS_URL = (
    "https://raw.githubusercontent.com/appinnovationmc-stack/eesyload-rider/"
    "656d5bdf3fbc/www/user-supabase-integration.js"
)

def restore_js():
    text = JS.read_text(encoding="utf-8") if JS.exists() else ""
    needs = (
        len(text) < 500
        or "PLACEHOLDER" in text
        or "async function createBooking" not in text
        or "payment_method" not in text
    )
    if needs:
        print("Restoring www/user-supabase-integration.js from last known good commit…")
        with urllib.request.urlopen(GOOD_JS_URL, timeout=30) as r:
            text = r.read().decode("utf-8")
        if "async function createBooking" not in text:
            print("Restore failed — bad download", file=sys.stderr)
            sys.exit(1)

    # scheduled_for on createBooking body
    old = "      payment_method: booking.payment_method || 'paystack_card',\n    }),"
    new = (
        "      payment_method: booking.payment_method || 'paystack_card',\n"
        "      scheduled_for: booking.scheduled_for || null,\n"
        "    }),"
    )
    if "scheduled_for: booking.scheduled_for" not in text:
        if old not in text:
            print("! createBooking body pattern missing", file=sys.stderr)
        else:
            text = text.replace(old, new, 1)
            print("✓ createBooking sends scheduled_for")
    else:
        print("✓ createBooking already sends scheduled_for")

    append = '''

/** Persist rider star rating onto the booking (driver_rating column). */
async function rateBookingDriver(bookingId, stars) {
  const user = await sbGetCurrentUser();
  if (!user) throw new Error('Not signed in');
  const n = Math.max(1, Math.min(5, Number(stars) || 0));
  if (!bookingId) throw new Error('No booking to rate');
  const { error } = await sb.from('bookings')
    .update({ driver_rating: n })
    .eq('id', bookingId)
    .eq('rider_id', user.id);
  if (error) throw error;
  return n;
}

/** Submit a business account application as a support ticket for admin review. */
async function submitBusinessApplicationToSupabase({ company_name, registration, email, phone, notes }) {
  const user = await sbGetCurrentUser();
  if (!user) throw new Error('Not signed in');
  const subject = 'Business account application: ' + (company_name || 'Unknown');
  const message = [
    'Company: ' + (company_name || '\u2014'),
    'Registration: ' + (registration || '\u2014'),
    'Email: ' + (email || '\u2014'),
    'Phone: ' + (phone || '\u2014'),
    notes ? ('Notes: ' + notes) : null,
  ].filter(Boolean).join('\n');
  const { data, error } = await sb.from('support_tickets').insert({
    user_id: user.id,
    subject,
    message,
    status: 'open',
    priority: 'normal',
  }).select().single();
  if (error) throw error;
  return data;
}
'''
    if "function rateBookingDriver" not in text:
        text = text.rstrip() + "\n" + append + "\n"
        print("✓ rateBookingDriver + business ticket helpers added")
    else:
        print("✓ helpers already present")

    JS.parent.mkdir(parents=True, exist_ok=True)
    JS.write_text(text, encoding="utf-8")
    print(f"Wrote {JS} ({len(text)} bytes)")


def patch_html():
    if not HTML.exists():
        print("www/index.html missing", file=sys.stderr)
        return
    text = HTML.read_text(encoding="utf-8")
    orig = text

    old_cb = """      paystack_reference: window._pendingPaystackRef || null,
      payment_method: AppState.paymentMethod || 'paystack_card'
    });"""
    new_cb = """      paystack_reference: window._pendingPaystackRef || null,
      payment_method: AppState.paymentMethod || 'paystack_card',
      scheduled_for: AppState.scheduledFor || null
    });"""
    if "scheduled_for: AppState.scheduledFor" not in text and old_cb in text:
        text = text.replace(old_cb, new_cb, 1)
        print("✓ HTML createBooking passes scheduled_for")
    elif "scheduled_for: AppState.scheduledFor" in text:
        print("✓ HTML already passes scheduled_for")
    else:
        print("! HTML createBooking block not found", file=sys.stderr)

    old_sch = """function confirmScheduledLoad(){
  if(!schedSelectedDate||!schedSelectedTime){
    alert('Please select a date and time slot first.');
    return;
  }
  AppState.scheduled=true;
  AppState.scheduledDate=schedSelectedDate;
  AppState.scheduledTime=schedSelectedTime;
  go('confirm');
}"""
    new_sch = """function confirmScheduledLoad(){
  if(!schedSelectedDate||!schedSelectedTime){
    alert('Please select a date and time slot first.');
    return;
  }
  AppState.scheduled=true;
  AppState.scheduledDate=schedSelectedDate;
  AppState.scheduledTime=schedSelectedTime;
  try{
    const monthLbl=(document.getElementById('calMonth')||{}).textContent||'';
    const yearMatch=monthLbl.match(/(\d{4})/);
    const year=yearMatch?yearMatch[1]:String(new Date().getFullYear());
    const dayMatch=String(schedSelectedDate).match(/(\d{1,2})\s*$/);
    const day=dayMatch?dayMatch[1]:'1';
    const monthNames={january:0,february:1,march:2,april:3,may:4,june:5,july:6,august:7,september:8,october:9,november:10,december:11};
    const monKey=String(schedSelectedDate).toLowerCase().replace(/[^a-z]/g,'');
    let month=null;
    for(const k in monthNames){if(monKey.startsWith(k.slice(0,3))||monKey.includes(k)){month=monthNames[k];break;}}
    if(month==null){
      const fromLbl=monthLbl.toLowerCase();
      for(const k in monthNames){if(fromLbl.includes(k)){month=monthNames[k];break;}}
    }
    let hours=9, minutes=0;
    const t=String(schedSelectedTime).trim();
    const ampm=t.match(/(\d{1,2}):(\d{2})\s*(AM|PM)?/i);
    if(ampm){
      hours=parseInt(ampm[1],10); minutes=parseInt(ampm[2],10);
      if(ampm[3]){
        const ap=ampm[3].toUpperCase();
        if(ap==='PM'&&hours<12)hours+=12;
        if(ap==='AM'&&hours===12)hours=0;
      }
    }
    if(month==null)month=new Date().getMonth();
    const local=new Date(Number(year), month, Number(day), hours, minutes, 0);
    AppState.scheduledFor=!isNaN(local.getTime())?local.toISOString():null;
  }catch(e){console.error(e);AppState.scheduledFor=null;}
  go('confirm');
}"""
    if "AppState.scheduledFor=" in text and "confirmScheduledLoad" in text:
        print("✓ confirmScheduledLoad already builds ISO (or partially)")
    elif old_sch in text:
        text = text.replace(old_sch, new_sch, 1)
        print("✓ confirmScheduledLoad builds scheduledFor ISO")
    else:
        print("! confirmScheduledLoad not found", file=sys.stderr)

    old_rate = """function rateStar(n){
  currentRating=n;
  document.querySelectorAll('#stars .star-btn').forEach((b,i)=>{
    if(i<n){b.classList.add('lit');b.innerHTML='<svg width="22" height="22" viewBox="0 0 24 22"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z" fill="var(--ylw)"/></svg>';}
    else{b.classList.remove('lit');b.innerHTML='<svg width="22" height="22" viewBox="0 0 24 22"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z" stroke="var(--ylw)" stroke-width="1.5" fill="none"/></svg>';}
  });
  // update the just-saved load with the rating
  const loads=getLoads();
  if(loads.length){loads[0].rating=n;localStorage.setItem('el-loads',JSON.stringify(loads));}
}"""
    new_rate = """function rateStar(n){
  currentRating=n;
  document.querySelectorAll('#stars .star-btn').forEach((b,i)=>{
    if(i<n){b.classList.add('lit');b.innerHTML='<svg width="22" height="22" viewBox="0 0 24 22"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z" fill="var(--ylw)"/></svg>';}
    else{b.classList.remove('lit');b.innerHTML='<svg width="22" height="22" viewBox="0 0 24 22"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z" stroke="var(--ylw)" stroke-width="1.5" fill="none"/></svg>';}
  });
  const loads=getLoads();
  if(loads.length){loads[0].rating=n;localStorage.setItem('el-loads',JSON.stringify(loads));}
  const bookingId=AppState.currentBookingId||(AppState.currentBooking&&AppState.currentBooking.id);
  if(bookingId&&typeof rateBookingDriver==='function'){
    rateBookingDriver(bookingId,n).catch(e=>console.error('Could not save rating',e));
  }
}"""
    if "rateBookingDriver(bookingId,n)" in text:
        print("✓ rateStar already persists")
    elif old_rate in text:
        text = text.replace(old_rate, new_rate, 1)
        print("✓ rateStar saves to DB")
    else:
        print("! rateStar block not found", file=sys.stderr)

    old_biz = """function submitBusinessApplication(){
  const name=document.getElementById('bizName').value.trim();
  const reg=document.getElementById('bizReg').value.trim();
  const email=document.getElementById('bizEmail').value.trim();
  if(!name||!reg||!email){
    alert('Please fill in company name, registration number, and business email.');
    return;
  }
  if(!/^\\S+@\\S+\\.\\S+$/.test(email)){
    alert('Please enter a valid business email address.');
    return;
  }
  alert('Business account application submitted for '+name+'. We will verify your details within 24 hours.');
  go('profile');
}"""
    # Fix regex - the source uses /^\S+@\S+\.\S+$/
    import re
    m = re.search(
        r"function submitBusinessApplication\(\)\{[\s\S]*?go\('profile'\);\n\}",
        text,
    )
    if m and "submitBusinessApplicationToSupabase" not in m.group(0):
        new_biz = """async function submitBusinessApplication(){
  const name=(document.getElementById('bizName')||{}).value?.trim()||'';
  const reg=(document.getElementById('bizReg')||{}).value?.trim()||'';
  const email=(document.getElementById('bizEmail')||{}).value?.trim()||'';
  const phone=(document.getElementById('bizPhone')||{}).value?.trim()||'';
  if(!name||!reg||!email){
    alert('Please fill in company name, registration number, and business email.');
    return;
  }
  if(!/^\\S+@\\S+\\.\\S+$/.test(email)){
    alert('Please enter a valid business email address.');
    return;
  }
  try{
    if(typeof submitBusinessApplicationToSupabase==='function'){
      await submitBusinessApplicationToSupabase({company_name:name,registration:reg,email:email,phone:phone});
    }
    alert('Business account application submitted for '+name+'. We will verify your details within 24 hours.');
    go('profile');
  }catch(e){
    console.error(e);
    alert('Could not submit application: '+(e.message||e));
  }
}"""
        # Use actual single-backslash regex in output file
        new_biz = new_biz.replace("\\\\S", "\\S").replace("\\\\.", "\\.")
        text = text[: m.start()] + new_biz + text[m.end() :]
        print("✓ business application writes support ticket")
    elif "submitBusinessApplicationToSupabase" in text:
        print("✓ business already wired")
    else:
        print("! business submit not found", file=sys.stderr)

    if "scheduledFor:null" not in text and "scheduledTime:null," in text:
        text = text.replace("scheduledTime:null,", "scheduledTime:null,\n  scheduledFor:null,", 1)
        print("✓ AppState.scheduledFor added")

    if text != orig:
        HTML.write_text(text, encoding="utf-8")
        print("Wrote", HTML)
    else:
        print("HTML unchanged")


if __name__ == "__main__":
    restore_js()
    patch_html()
    print("\nNext: git add www/user-supabase-integration.js www/index.html && git commit && git push")
