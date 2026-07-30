with open('user-supabase-integration.js', 'r') as f:
    content = f.read()

marker = "/* ─── SAVED ADDRESSES ────────────────────────────────────── */"

addition = """/* ─── REFERRALS ──────────────────────────────────────────── */
async function getMyReferralCode() {
  const user = await sbGetCurrentUser();
  if (!user) throw new Error('Not signed in');
  const { data, error } = await sb.from('profiles')
    .select('referral_code,referred_by').eq('id', user.id).single();
  if (error) throw error;
  return data;
}

async function applyReferralCode(code) {
  const user = await sbGetCurrentUser();
  if (!user) throw new Error('Not signed in');

  const { data: ownerId, error: rpcError } = await sb.rpc('resolve_referral_code', { code });
  if (rpcError) throw rpcError;
  if (!ownerId) throw new Error('That referral code was not found.');
  if (ownerId === user.id) throw new Error("You can't use your own referral code.");

  const { error } = await sb.from('profiles')
    .update({ referred_by: ownerId }).eq('id', user.id);
  if (error) throw error;
  return true;
}

""" + marker

if marker not in content:
    print("ERROR: marker not found")
else:
    content = content.replace(marker, addition, 1)
    with open('user-supabase-integration.js', 'w') as f:
        f.write(content)
    print("SUCCESS: referral functions added")
