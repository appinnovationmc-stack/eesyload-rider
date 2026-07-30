with open('index.html', 'r') as f:
    content = f.read()

old = """async function renderRefCode(){
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

new = """async function renderRefCode(){
  const el=document.getElementById('ref-code');
  if(!el)return;
  el.textContent='...';
  try{
    const profile=await getMyReferralCode();
    el.textContent=profile.referral_code||'—';
    const enterBox=document.getElementById('enterCodeBox');
    if(enterBox){
      enterBox.style.display=profile.referred_by?'none':'block';
    }
  }catch(e){
    console.error('Could not load referral code',e);
    el.textContent='—';
  }
}

async function submitFriendCode(){
  const input=document.getElementById('friendCodeInput');
  const msg=document.getElementById('friendCodeMsg');
  if(!input||!input.value.trim())return;
  const code=input.value.trim().toUpperCase();
  if(msg){msg.style.color='var(--g60)';msg.textContent='Checking code…';}
  try{
    await applyReferralCode(code);
    if(msg){msg.style.color='#06C167';msg.textContent='Referral applied! Thanks for joining through a friend.';}
    setTimeout(()=>{
      const enterBox=document.getElementById('enterCodeBox');
      if(enterBox)enterBox.style.display='none';
    },1500);
  }catch(e){
    if(msg){msg.style.color='#FF3B30';msg.textContent=e.message||'Could not apply that code.';}
  }
}"""

if old not in content:
    print("ERROR: exact match not found")
else:
    content = content.replace(old, new, 1)
    with open('index.html', 'w') as f:
        f.write(content)
    print("SUCCESS: submitFriendCode added, renderRefCode hides box if already referred")
