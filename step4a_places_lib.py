with open('index.html', 'r') as f:
    content = f.read()

old = "s.src='https://maps.googleapis.com/maps/api/js?key=AIzaSyBAUx4OpJivUYKzeh0Ol7zFjIlHY4czQQM&v=weekly';"
new = "s.src='https://maps.googleapis.com/maps/api/js?key=AIzaSyBAUx4OpJivUYKzeh0Ol7zFjIlHY4czQQM&v=weekly&libraries=places';"

if old not in content:
    print("ERROR: exact match not found")
else:
    content = content.replace(old, new, 1)
    with open('index.html', 'w') as f:
        f.write(content)
    print("SUCCESS: places library added to maps script")
