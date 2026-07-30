with open('index.html', 'r') as f:
    content = f.read()

old = """async function renderHistoryList(){
  const container=document.getElementById('historyList');
  if(!container)return;
  try{
    const {data:sess} = await sb.auth.getSession();
    const token = sess?.session?.access_token || 'NO TOKEN';
    container.innerHTML = `<div style="padding:20px;color:#fff;font-size:11px;word-break:break-all;">TOKEN: ${token}</div>`;
  }catch(e){
    container.innerHTML = `<div style="padding:20px;color:red;">DEBUG error: ${e.message}</div>`;
  }
  return;
  await refreshLoads();"""

new = """async function renderHistoryList(){
  const container=document.getElementById('historyList');
  if(!container)return;
  await refreshLoads();"""

if old not in content:
    print("ERROR: exact match not found")
else:
    content = content.replace(old, new, 1)
    with open('index.html', 'w') as f:
        f.write(content)
    print("SUCCESS: debug token dump removed, real history rendering restored")
