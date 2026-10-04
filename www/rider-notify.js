(function () {
  var P = window.Capacitor && window.Capacitor.Plugins && window.Capacitor.Plugins.PushNotifications;
  if (!P || !(window.Capacitor.isNativePlatform && window.Capacitor.isNativePlatform())) return;
  var lastToken = null, registered = false;

  async function saveToken(token) {
    try {
      var s = await sb.auth.getSession();
      if (!s.data || !s.data.session) return;
      var r = await sb.rpc('register_device_token', { p_token: token, p_app: 'rider' });
      if (r.error) console.error('register_device_token', r.error);
    } catch (e) { console.error('saveToken', e); }
  }

  async function init() {
    if (registered) { if (lastToken) saveToken(lastToken); return; }
    try {
      var perm = await P.checkPermissions();
      if (perm.receive === 'prompt' || perm.receive === 'prompt-with-rationale') perm = await P.requestPermissions();
      if (perm.receive !== 'granted') return;
      registered = true;
      try {
        await P.createChannel({ id: 'trip_updates', name: 'Trip updates', description: 'Updates on your load', importance: 4, visibility: 1, sound: 'default', vibration: true });
      } catch (e) {}
      P.addListener('registration', function (t) { lastToken = t.value; saveToken(t.value); });
      P.addListener('registrationError', function (e) { console.error('push registrationError', e); });
      P.addListener('pushNotificationReceived', function (n) {
        var msg = (n.title ? n.title + ': ' : '') + (n.body || '');
        if (typeof showToast === 'function') showToast(msg); else console.log('push', msg);
      });
      await P.register();
    } catch (e) { console.error('push init', e); }
  }

  function boot() {
    sb.auth.getSession().then(function (s) { if (s.data && s.data.session) init(); });
    sb.auth.onAuthStateChange(function (ev, session) { if (session) init(); });
  }
  if (typeof sb !== 'undefined') boot(); else window.addEventListener('load', function () { if (typeof sb !== 'undefined') boot(); });
})();
