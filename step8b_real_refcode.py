with open('index.html', 'r') as f:
    content = f.read()

old = """function renderRefCode(){
  const el=document.getElementById('ref-code');
  if(!el)return;
  let code=localStorage.getItem('el-ref-code');
  if(!code){
    // TODO: replace with server-issued code once auth/backend is wired in
    code='EL-'+Math.random().toString(36).slice(2,8).toUpperCase();
    localStorage.setItem('el-ref-code',code);
  }
  el.textContent=code;
}"""

new = """async function renderRefCode(){
  const el=document.getElementById('ref-code');
  if(!el)return;
  el.textContent='...';
  try{
    const profile=await getMyReferralCode();
    el.textContent=profile.referral_code||'—';
  }catch(e){
    console.error('Could not load referral code',e);
    el.textContent='—';
  }
}"""

if old not in content:
    print("ERROR: exact match not found")
else:
    content = content.replace(old, new, 1)
    with open('index.html', 'w') as f:
        f.write(content)
    print("SUCCESS: renderRefCode now uses real server-issued code")
