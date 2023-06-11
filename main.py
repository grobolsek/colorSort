from PIL import Image
import png
import random
import colorsys
import math


def create_img():

    height = 1024
    width = 2048
    colors = []
    for r in range(0, 256, 2):
        for g in range(0, 256, 2):
            for b in range(0, 256, 2):
                colors.append((r, g, b))

    random.shuffle(colors)

    img = []
    for i in range(height):
        row = ()
        for j in range(width):
            row = row + colors[i*width+j]
        img.append(row)

    with open('gradient_random.png', 'wb') as f:
        w = png.Writer(width, height, greyscale=False)
        w.write(f, img)


# create_img()


def rec_lists(items: list) -> list:
    value = []
    for item in items:
        if not isinstance(item, list):
            value.append(item)
        else:
            value.extend(rec_lists(item))

    return value


def avg(values: list) -> int:
    return sum(x := rec_lists(values))/len(x)


def get_image_avg(name: str) -> list:
    """
    :param name: directory of the picture
    :return: average of the picture
    """
    rgb = []
    im = Image.open(name)
    im = im.convert('RGBA')
    pix = im.load()
    size = im.size
    for x in range(size[0]):
        for y in range(size[1]):
            c = pix[x, y]
            rgb.append(c)

    return rgb


def lum(r, g, b):
    return math.sqrt(.241 * r + .691 * g + .068 * b)


def create_img_s(name: str):
    rgb = get_image_avg(name)
    # rgb_s = sorted(rgb, key=lambda x: colorsys.rgb_to_hsv(*x[:3]))
    # x[0]+x[1]+x[2]
    # x[0] - x[1] - x[2], -x[0] + x[1] - x[2], -x[0] - x[1] + x[2]
    # (colorsys.rgb_to_hsv(*x[:3])[2]/255 - colorsys.rgb_to_hsv(*x[:3])[1])//(1/10)
    # h -> 0-1 hue, s -> 0-1 white, v -> 0-255 black
    rgb_s = sorted(rgb, key=lambda x: (colorsys.rgb_to_hsv(*x[:3])[0]//(1/2**4), (abs(x[0]-(x[0]+x[1]+x[2])/3) + abs(x[1]-(x[0]+x[1]+x[2])/3) + abs(x[2]-(x[0]+x[1]+x[2])/3))-2*((x[0]+x[1]+x[2])/3)))

    # TODO: sort by lum for each column

    im = Image.open(name)
    im = im.convert('RGBA')
    pix = im.load()
    size = im.size
    for x in range(size[0]):
        for y in range(size[1]):
            pix[x, y] = rgb_s[x*size[1]+y]
    im.save('sorted.png')


create_img_s('gradient_random.png')
