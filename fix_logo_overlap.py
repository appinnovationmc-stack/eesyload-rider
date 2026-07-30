with open('index.html', 'r') as f:
    content = f.read()

old = ".home-logo-img{display:flex;align-items:center;}"
new = ".home-logo-img{display:flex;align-items:center;background:rgba(0,0,0,.65);backdrop-filter:blur(10px);border:1px solid rgba(255,255,255,.1);border-radius:100px;padding:6px 14px 6px 8px;height:40px;box-sizing:border-box;}\n.home-logo-img .logo-svg{height:26px;width:auto;}"

if old not in content:
    print("ERROR: exact match not found")
else:
    content = content.replace(old, new, 1)
    with open('index.html', 'w') as f:
        f.write(content)
    print("SUCCESS: home logo given proper background pill")
