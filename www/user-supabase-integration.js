/* Rider integration from uploaded zip (2026-07-30). Same project as driver. */
const SUPABASE_URL = 'https://mbtqqnbklcltrtwlpduq.supabase.co';
const SUPABASE_ANON_KEY = 'sb_publishable_ff0SBElpjzVkCaHyPHAYUQ_1sOCyRES';
const sb = supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);

async function sbSendOtp(phone) {
  const { error } = await sb.auth.signInWithOtp({ phone });
  if (error) throw error;
}

async function sbVerifyOtp(phone, token) {
  const { data, error } = await sb.auth.verifyOtp({ phone, token, type: 'sms' });
  if (error) throw error;
  const { data: existing } = await sb.from('profiles').select('id').eq('id', data.user.id).maybeSingle();
  if (!existing) {
    await sb.from('profiles').insert({ id: data.user.id, role: 'rider', phone });
  }
  return data.user;
}

async function sbGetCurrentUser() {
  const { data } = await sb.auth.getUser();
  return data.user;
}

async function sbSignOut() {
  const { error } = await sb.auth.signOut();
  if (error) throw error;
}
