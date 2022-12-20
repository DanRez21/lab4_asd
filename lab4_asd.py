from PIL import Image, ImageDraw

import random

w = 960
h = 540

def get_neighbours(point):
    x, y = point

    yield (x+1, y)
    yield (x-1, y)
    yield (x, y+1)
    yield (x, y-1)

    yield (x+1, y+1)
    yield (x-1, y-1)
    yield (x-1, y+1)
    yield (x+1, y-1)


def avg(points):
    x, y = 0.0, 0.0

    l = float(len(points))

    for i in points:
        xi, yi = i
        x += xi/l
        y += yi/l

    return int(x), int(y)


def bfs(p, points):

    visited = {p}
    q = [p]

    while len(q) > 0:
        node = q.pop(0)
        for n in get_neighbours(node):
            if n in points and n not in visited:
                q.append(n)
                visited.add(n)
                
    return visited


def divide(points):
    chunks = []

    while len(points) > 0:

        p = next(iter(points))
        chunk = bfs(p, points)

        for c in chunk:
            points.remove(c)

        chunks.append(chunk)

    return chunks

def circle(draw, center, radius, fill):

    x, y = center
    draw.ellipse((x-radius, y-radius, x+radius, y+radius), fill)
    
def sqr_dist(a, b):

    x = a[0] - b[0]
    y = a[1] - b[1]

    return x * x + y * y
    

def random_color():
    return (
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255)
    )

with open('DS0.txt') as f:

    img = Image.new('RGBA', (w, h), '#ffffff')
    draw = ImageDraw.Draw(img)

    points = []

    for i in f.readlines():
        coord = i.split(' ')
        points.append((int(coord[1]), int(coord[0])))

    for p in points:
        draw.point(p, '#000000')

    chunks = list(map(avg, divide(set(points))))

    colors = {i: random_color() for i in chunks}

    for x in range(w):
        for y in range(h):
            color = colors[min(chunks, key=lambda a: sqr_dist((x, y), a))]
            draw.point((x,y), color)

    alpha_img = Image.new('RGBA', (w, h), (0,0,0,0))
    alpha_draw = ImageDraw.Draw(alpha_img)

    for i in points:
        alpha_draw.point(i, (0, 0, 0, 25))

    for i in chunks:
        circle(draw, i, 2.5, '#ffffff')

    Image.alpha_composite(img, alpha_img).save('result4.png')

        