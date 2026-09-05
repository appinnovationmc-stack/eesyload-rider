/* Shared EesyLoad vehicle icons. currentColor so light/dark both work. */
(function (g) {
  const svg = {
    bike: '<svg width="40" height="24" viewBox="0 0 42 26" fill="none"><circle cx="9" cy="20" r="5.5" stroke="currentColor" stroke-width="1.8"/><circle cx="33" cy="20" r="5.5" stroke="currentColor" stroke-width="1.8"/><path d="M14.5 20H27.5M21 20V9" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/><path d="M15 9h12l4 6H11l4-6z" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/><path d="M21 9V4l5-3" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>',
    bakkie: '<svg width="40" height="24" viewBox="0 0 50 28" fill="none"><rect x="14" y="3" width="32" height="16" rx="2.5" stroke="currentColor" stroke-width="1.8"/><path d="M3 13h11l5-10h6" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/><path d="M2 13v8h47v-8" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/><circle cx="12" cy="24" r="4" stroke="currentColor" stroke-width="1.8"/><circle cx="39" cy="24" r="4" stroke="currentColor" stroke-width="1.8"/></svg>',
    van: '<svg width="40" height="24" viewBox="0 0 50 28" fill="none"><path d="M2 20V11c0-2 1.5-4 3-4L22 4h22a3 3 0 013 3v13" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/><path d="M2 20h46" stroke="currentColor" stroke-width="1.8"/><rect x="6" y="7" width="9" height="7" rx="1.5" stroke="currentColor" stroke-width="1.5"/><rect x="18" y="7" width="9" height="7" rx="1.5" stroke="currentColor" stroke-width="1.5"/><circle cx="11" cy="24" r="4" stroke="currentColor" stroke-width="1.8"/><circle cx="37" cy="24" r="4" stroke="currentColor" stroke-width="1.8"/></svg>',
    truck: '<svg width="40" height="24" viewBox="0 0 52 28" fill="none"><rect x="2" y="4" width="32" height="16" rx="2" stroke="currentColor" stroke-width="1.8"/><path d="M34 9h12l5 8v4H34V9z" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/><circle cx="11" cy="24" r="4" stroke="currentColor" stroke-width="1.8"/><circle cx="26" cy="24" r="4" stroke="currentColor" stroke-width="1.8"/><circle cx="43" cy="24" r="4" stroke="currentColor" stroke-width="1.8"/></svg>'
  };
  function key(name) {
    const s = String(name || '').toLowerCase();
    if (s.includes('moto') || s.includes('bike')) return 'bike';
    if (s.includes('bakkie') || s.includes('pickup')) return 'bakkie';
    if (s.includes('van') || s.includes('panel')) return 'van';
    if (s.includes('ton') || s.includes('truck') || s.includes('flat')) return 'truck';
    return 'truck';
  }
  g.eesyVehicleIcon = function (name) { return svg[key(name)]; };
  g.eesyVehicleKey = key;
  if (typeof _vehicleIconMap === 'object') {
    const old = _vehicleIconMap;
    g._vehicleIconMap = new Proxy(old, {
      get: function (t, prop) {
        if (prop === '_default_truck') return svg.truck;
        if (typeof prop === 'string') return svg[key(prop)];
        return t[prop];
      }
    });
  }
})(window);
