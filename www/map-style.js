window.EESY_DARK_MAP = [
  { elementType: 'geometry', stylers: [{ color: '#1c1c1e' }] },
  { elementType: 'labels.text.fill', stylers: [{ color: '#8e8e93' }] },
  { elementType: 'labels.text.stroke', stylers: [{ color: '#1c1c1e' }] },
  { featureType: 'administrative', elementType: 'geometry', stylers: [{ visibility: 'off' }] },
  { featureType: 'poi', stylers: [{ visibility: 'off' }] },
  { featureType: 'poi.park', stylers: [{ visibility: 'off' }] },
  { featureType: 'road', elementType: 'geometry', stylers: [{ color: '#2c2c2e' }] },
  { featureType: 'road', elementType: 'geometry.stroke', stylers: [{ color: '#000000' }] },
  { featureType: 'road.highway', elementType: 'geometry', stylers: [{ color: '#3a3a3c' }] },
  { featureType: 'transit', stylers: [{ visibility: 'off' }] },
  { featureType: 'water', stylers: [{ color: '#000000' }] }
];
window.eesyMapOptions = function (extra) {
  const light = document.documentElement.dataset.theme === 'light';
  return Object.assign({
    disableDefaultUI: true,
    zoomControl: false,
    mapTypeControl: false,
    streetViewControl: false,
    fullscreenControl: false,
    gestureHandling: 'greedy',
    styles: light ? [{ featureType: 'poi', stylers: [{ visibility: 'off' }] }] : window.EESY_DARK_MAP
  }, extra || {});
};
window.eesyApplyMapStyle = function (map) {
  if (!map || !window.google) return;
  map.setOptions(window.eesyMapOptions());
};
window.eesyPin = function (kind) {
  const color = kind === 'drop' ? '#BB2235' : kind === 'driver' ? '#F5F5F7' : '#34C759';
  return {
    path: window.google && google.maps.SymbolPath.CIRCLE,
    scale: kind === 'driver' ? 8 : 7,
    fillColor: color,
    fillOpacity: 1,
    strokeColor: '#000',
    strokeWeight: 1.5
  };
};
window.eesyOpenTurnByTurn = function (address) {
  if (!address) return;
  const q = encodeURIComponent(address);
  const url = 'https://www.google.com/maps/dir/?api=1&destination=' + q + '&travelmode=driving';
  window.open(url, '_blank');
};
