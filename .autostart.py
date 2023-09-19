import os

start = [
        "volumeicon &",
        "picom &",
        "feh --bg-scale Dropbox/love-death-robots-wall.jpg",
        "megasync &",
        "dropbox &",
]

for x in start:
    os.system(x)

