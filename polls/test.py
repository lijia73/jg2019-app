import os
listevent = []
for root, dirs, files in os.walk("../static/event"):
    for file in files: 
        listevent.append(os.path.splitext(file)[0])
print(listevent)
