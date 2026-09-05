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
  function trackingDest() {
    const st = (window.AppState && (AppState.currentBooking && AppState.currentBooking.status)) || '';
    if (st === 'in_transit' || st === 'loading') return AppState.dropoff || AppState.dropoff_address;
    return AppState.pickup || AppState.pickup_address;
  }
  const origRoute = window.routeAndUpdateEta;
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
