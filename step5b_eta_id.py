with open('index.html', 'r') as f:
    content = f.read()

old = '<div class="eta-pill"><div class="eta-t">8 min</div><div class="eta-l">Driver arriving</div></div>'
new = '<div class="eta-pill"><div class="eta-t" id="trkEtaText">--</div><div class="eta-l">Driver arriving</div></div>'

if old not in content:
    print("ERROR: exact match not found")
else:
    content = content.replace(old, new, 1)
    with open('index.html', 'w') as f:
        f.write(content)
    print("SUCCESS: eta pill given an id")
