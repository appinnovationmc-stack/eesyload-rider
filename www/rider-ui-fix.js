(function () {
  function applyTheme(t) {
    if (t !== 'light' && t !== 'dark') t = 'dark';
    document.documentElement.dataset.theme = t;
    try { localStorage.setItem('el-theme', t); } catch (e) {}
    const sw = document.getElementById('themeSwitch');
    if (sw) sw.checked = t === 'light';
    styleHomeMap();
    paintVehicleIcons();
  }
  function bootTheme() {
    let t = null;
    try { t = localStorage.getItem('el-theme'); } catch (e) {}
    if (!t) t = window.matchMedia && window.matchMedia('(prefers-color-scheme: light)').matches ? 'light' : 'dark';
    applyTheme(t);
  }
  const darkMap = [
    { elementType: 'geometry', stylers: [{ color: '#1c1c1e' }] },
    { elementType: 'labels.text.fill', stylers: [{ color: '#8e8e93' }] },
    { featureType: 'poi', stylers: [{ visibility: 'off' }] },
    { featureType: 'road', elementType: 'geometry', stylers: [{ color: '#2c2c2e' }] },
    { featureType: 'water', stylers: [{ color: '#000000' }] }
  ];
  function styleHomeMap() {
    if (!window.homeMap || !window.google) return;
    const light = document.documentElement.dataset.theme === 'light';
    homeMap.setOptions({ disableDefaultUI: true, zoomControl: false, styles: light ? [] : darkMap });
  }
  function paintVehicleIcons() {
    document.querySelectorAll('.vc-ill svg, .ti svg').forEach(function (svg) {
      svg.setAttribute('stroke', 'currentColor');
      svg.querySelectorAll('[stroke]').forEach(function (n) {
        n.setAttribute('stroke', 'currentColor');
      });
      svg.style.color = 'inherit';
    });
  }
  function injectProfileToggle() {
    const prof = document.getElementById('profile');
    if (!prof || document.getElementById('themeRow')) return;
    const msec = prof.querySelector('.msec');
    if (!msec) return;
    const row = document.createElement('div');
    row.className = 'row';
    row.id = 'themeRow';
    row.innerHTML = '<div class="rb"><div class="rt">Appearance</div><div class="rs">Light / dark</div></div><label class="theme-switch"><input id="themeSwitch" type="checkbox"><span></span></label>';
    msec.appendChild(row);
    const sw = document.getElementById('themeSwitch');
    sw.checked = document.documentElement.dataset.theme === 'light';
    sw.addEventListener('change', function () { applyTheme(sw.checked ? 'light' : 'dark'); });
  }
  document.addEventListener('DOMContentLoaded', function () {
    bootTheme();
    injectProfileToggle();
    setTimeout(styleHomeMap, 800);
    setTimeout(paintVehicleIcons, 400);
    setTimeout(paintVehicleIcons, 1600);
    const row = document.getElementById('vcRow');
    if (row && window.MutationObserver) {
      new MutationObserver(paintVehicleIcons).observe(row, { childList: true, subtree: true });
    }
  });
  const origGo = window.go;
  if (origGo) {
    window.go = function (id) {
      origGo(id);
      if (id === 'profile') injectProfileToggle();
      if (id === 'home') setTimeout(styleHomeMap, 300);
      if (id === 'booking') setTimeout(paintVehicleIcons, 200);
    };
  }
  window.eesyApplyTheme = applyTheme;
})();
