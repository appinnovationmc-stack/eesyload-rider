(function () {
  function styleAll() {
    if (typeof eesyApplyMapStyle !== 'function') return;
    if (window.homeMap) eesyApplyMapStyle(homeMap);
    if (window.trkMap) eesyApplyMapStyle(trkMap);
    if (window.trkDirRenderer && window.google) {
      trkDirRenderer.setOptions({ polylineOptions: { strokeColor: '#BB2235', strokeWeight: 5 } });
    }
    if (window.trkDriverMarker && window.google) {
      try { trkDriverMarker.setIcon(eesyPin('driver')); } catch (e) {}
    }
  }
  // Match driver phases: pickup until in_transit, then drop-off
  function trackingDest() {
    const st =
      (window.AppState &&
        (AppState.bookingStatus ||
          (AppState.currentBooking && AppState.currentBooking.status))) ||
      '';
    if (st === 'in_transit') {
      if (AppState.dropoffLat != null && AppState.dropoffLng != null) {
        return { lat: Number(AppState.dropoffLat), lng: Number(AppState.dropoffLng) };
      }
      return AppState.dropoff || AppState.dropoff_address || null;
    }
    if (AppState.pickupLat != null && AppState.pickupLng != null) {
      return { lat: Number(AppState.pickupLat), lng: Number(AppState.pickupLng) };
    }
    return AppState.pickup || AppState.pickup_address || null;
  }
  window.trackingDest = trackingDest;
  document.addEventListener('DOMContentLoaded', function () {
    setTimeout(styleAll, 600);
    setTimeout(styleAll, 2000);
    setInterval(styleAll, 8000);
  });
  const origGo = window.go;
  if (origGo) {
    window.go = function (id) {
      origGo(id);
      if (id === 'home' || id === 'tracking') setTimeout(styleAll, 400);
    };
  }
})();
