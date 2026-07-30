with open('index.html', 'r') as f:
    content = f.read()

old = '<canvas id="tc" width="393" height="340" style="position:absolute;inset:0;width:100%;height:100%;"></canvas>'
new = '<div id="trkmap" style="position:absolute;inset:0;width:100%;height:100%;"></div>'

if old not in content:
    print("ERROR: exact match not found")
else:
    content = content.replace(old, new, 1)
    with open('index.html', 'w') as f:
        f.write(content)
    print("SUCCESS: tracking canvas replaced with real map div")
