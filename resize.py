import json
from PIL import Image
import os
import sys
import smartcrop
from glob import glob

def remove_transparency(im, bg_colour=(255, 255, 255)):
    if im.mode in ('RGBA', 'LA') or (im.mode == 'P' and 'transparency' in im.info):
        alpha = im.convert('RGBA').split()[-1]
        bg = Image.new("RGBA", im.size, bg_colour + (255,))
        bg.paste(im, mask=alpha)
        return bg
    else:
        return im


SIZE = 200, 200
dataset_path = 'dataset_sample'

sc = smartcrop.SmartCrop()
crop_options = smartcrop.DEFAULTS
crop_options['width'] = 100 
crop_options['height'] = 100


files = glob(os.path.join(dataset_path, '*', '*.jpg'))
other = glob(os.path.join(dataset_path, '*', '*.png'))
files.extend(other)

for path in files:
    print(path)
    name, extension = os.path.splitext(path)
    img = Image.open(path)
    img = remove_transparency(img)

    crops = sc.crop(img.copy(), crop_options)
    best = crops['topCrop']
    x, y = best['x'], best['y'] 
    w, h = best['width'], best['height']

    img.crop((x, y, x+w, y+h)).convert('RGB').resize(SIZE).save(name + '_cropped.jpg')

print(files)
