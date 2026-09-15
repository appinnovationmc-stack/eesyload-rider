#!/usr/bin/env python3
"""Idempotent: fix rider tracking map destination by booking status."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
TARGET = ROOT / "www" / "index.html"

if not TARGET.exists():
    print("www/index.html not found", file=sys.stderr)
    sys.exit(1)

text = TARGET.read_text(encoding="utf-8")
orig = text
changed = []

# 1) Replace hard-coded pickup destination in routeAndUpdateEta
OLD_ROUTE = """  function routeAndUpdateEta(driverPos){
    const dest=AppState.pickup;
    if(!dest)return;
    const svc=new google.maps.DirectionsService();
    svc.route({origin:driverPos,destination:dest,travelMode:google.maps.TravelMode.DRIVING},(res,status)=>{
      if(status==='OK'){
        trkDirRenderer.setDirections(res);
        const leg=res.routes[0].legs[0];
        const etaEl=document.getElementById('trkEtaText');
        if(etaEl)etaEl.textContent=leg.duration.text;
        AppState.lastKnownEtaText=leg.duration.text;
      }
    });
  }"""

NEW_ROUTE = """  function trackingRouteDestination(){
    // Align with driver phases: en route to pickup until in_transit, then drop-off
    const st=(AppState.bookingStatus||(AppState.currentBooking&&AppState.currentBooking.status)||'');
    if(st==='in_transit'){
      if(AppState.dropoffLat!=null&&AppState.dropoffLng!=null){
        return {lat:Number(AppState.dropoffLat),lng:Number(AppState.dropoffLng)};
      }
      return AppState.dropoff||null;
    }
    if(AppState.pickupLat!=null&&AppState.pickupLng!=null){
      return {lat:Number(AppState.pickupLat),lng:Number(AppState.pickupLng)};
    }
    return AppState.pickup||null;
  }
  function routeAndUpdateEta(driverPos){
    const dest=trackingRouteDestination();
    if(!dest)return;
    const destKey=typeof dest==='string'?dest:(dest.lat+','+dest.lng);
    // Avoid spamming Directions when nothing meaningful changed
    if(AppState._trkLastDestKey===destKey&&AppState._trkLastOrigin){
      const o=AppState._trkLastOrigin;
      const dlat=Math.abs(o.lat-driverPos.lat)+Math.abs(o.lng-driverPos.lng);
      if(dlat<0.0003)return; // ~30m
    }
    AppState._trkLastDestKey=destKey;
    AppState._trkLastOrigin={lat:driverPos.lat,lng:driverPos.lng};
    const svc=new google.maps.DirectionsService();
    svc.route({origin:driverPos,destination:dest,travelMode:google.maps.TravelMode.DRIVING},(res,status)=>{
      if(status==='OK'){
        trkDirRenderer.setDirections(res);
        const leg=res.routes[0].legs[0];
        const etaEl=document.getElementById('trkEtaText');
        if(etaEl)etaEl.textContent=leg.duration.text;
        AppState.lastKnownEtaText=leg.duration.text;
        const phaseEl=document.getElementById('trkPhaseText');
        if(phaseEl){
          phaseEl.textContent=(AppState.bookingStatus==='in_transit')?'En route to drop-off':'Driver en route to you';
        }
      }
    });
  }
  // Expose so status changes can force a re-route
  window.routeAndUpdateEta=routeAndUpdateEta;
  window.trackingRouteDestination=trackingRouteDestination;"""

if "function trackingRouteDestination()" in text:
    print("✓ trackingRouteDestination already present")
elif OLD_ROUTE in text:
    text = text.replace(OLD_ROUTE, NEW_ROUTE, 1)
    changed.append("routeAndUpdateEta status-aware destination")
    print("✓ routeAndUpdateEta now switches pickup → drop-off on in_transit")
else:
    print("! Could not find routeAndUpdateEta block to patch", file=sys.stderr)

# 2) Track booking status on realtime updates + re-route when phase changes
OLD_SUB = """    AppState.bookingSub=subscribeToBookingUpdates(booking.id, async(updated)=>{
      if(updated.status==='accepted' && updated.driver_id){
"""

NEW_SUB = """    AppState.bookingSub=subscribeToBookingUpdates(booking.id, async(updated)=>{
      AppState.currentBooking=updated;
      const prevStatus=AppState.bookingStatus;
      AppState.bookingStatus=updated.status;
      // When phase flips to in_transit, force a new route to drop-off
      if(updated.status==='in_transit' && prevStatus!=='in_transit' && typeof window.routeAndUpdateEta==='function'){
        AppState._trkLastDestKey=null;
        if(AppState.driver&&trkDriverMarker){
          const pos=trkDriverMarker.getPosition();
          if(pos)window.routeAndUpdateEta({lat:pos.lat(),lng:pos.lng()});
        }
      }
      if(updated.status==='accepted' && updated.driver_id){
"""

if "AppState.bookingStatus=updated.status" in text:
    print("✓ bookingStatus tracking already present")
elif OLD_SUB in text:
    text = text.replace(OLD_SUB, NEW_SUB, 1)
    changed.append("status tracking + re-route on in_transit")
    print("✓ booking subscription tracks status and re-routes on in_transit")
else:
    print("! Could not find booking subscription block to patch", file=sys.stderr)

# 3) Add bookingStatus to AppState defaults if missing
if "bookingStatus:" in text or "bookingStatus," in text:
    print("✓ AppState.bookingStatus field present or set at runtime")
else:
    # best-effort: inject next to currentBookingId
    needle = "currentBookingId:null,"
    if needle in text:
        text = text.replace(needle, "currentBookingId:null,\n  bookingStatus:null,", 1)
        changed.append("AppState.bookingStatus default")
        print("✓ AppState.bookingStatus added")

# 4) Optional phase label on tracking screen (non-fatal if markup missing)
OLD_ETA_MARKUP_HINT = 'id="trkEtaText"'
if 'id="trkPhaseText"' in text:
    print("✓ trkPhaseText already in markup")
elif OLD_ETA_MARKUP_HINT in text:
    # Insert a small phase line near ETA if we can find a simple pattern
    # Keep conservative — only if exact known snippet exists
    pass

if text == orig:
    print("No changes needed (already applied or patterns drifted).")
    sys.exit(0)

TARGET.write_text(text, encoding="utf-8")
print("\nDone. Changes:", ", ".join(changed) if changed else "(see above)")
print("Review with: git diff www/index.html")
