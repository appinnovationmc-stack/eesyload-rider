with open('index.html', 'r') as f:
    content = f.read()

old = "  if(id==='tracking')requestAnimationFrame(startTrk);"
new = "  if(id==='tracking'){initTrackingMap();}else{stopTrackingMap();}"

if old not in content:
    print("ERROR: exact match not found")
else:
    content = content.replace(old, new, 1)
    with open('index.html', 'w') as f:
        f.write(content)
    print("SUCCESS: initTrackingMap wired into go(), replacing fake animation")
