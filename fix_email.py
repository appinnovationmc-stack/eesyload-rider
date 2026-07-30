with open('index.html', 'r') as f:
    content = f.read()

old = """  const emailForPaystack = (user.phone || user.id) + '@eesyload.rider';
  console.log('Paystack email:', emailForPaystack, 'user:', user);
  const handler = PaystackPop.setup({
    key: PAYSTACK_PUBLIC_KEY,
    email: emailForPaystack,"""

new = """  let rawIdentifier = (user && (user.phone || user.id)) ? (user.phone || user.id) : 'guest';
  let safeIdentifier = String(rawIdentifier).replace(/[^a-zA-Z0-9]/g, '');
  if(!safeIdentifier) safeIdentifier = 'rider' + Date.now();
  const emailForPaystack = safeIdentifier + '@eesyload.rider';
  console.log('Paystack email:', emailForPaystack, 'user:', user);
  const handler = PaystackPop.setup({
    key: PAYSTACK_PUBLIC_KEY,
    email: emailForPaystack,"""

if old not in content:
    print("ERROR: exact match not found")
else:
    content = content.replace(old, new, 1)
    with open('index.html', 'w') as f:
        f.write(content)
    print("SUCCESS: bulletproof email sanitization added")
