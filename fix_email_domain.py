with open('index.html', 'r') as f:
    content = f.read()

old = "const emailForPaystack = safeIdentifier + '@eesyload.rider';"
new = "const emailForPaystack = safeIdentifier + '@riders.eesyload.com';"

if old not in content:
    print("ERROR: exact match not found")
else:
    content = content.replace(old, new, 1)
    with open('index.html', 'w') as f:
        f.write(content)
    print("SUCCESS: email domain changed to riders.eesyload.com")
