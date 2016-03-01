#!/usr/bin/env python
# Copyright (C) 2012 by Kirik Konstantin <snegovick>

from sys import argv
import zbar
import Image, ImageDraw, ImageOps, ImageFont
import math

font = None

track_colors=[(255, 0, 0, 0), (0,255,0, 0), (0,0,255, 0), (255,255,0, 0), (0,255,255, 0), (255, 0, 255, 0), (128, 128, 128, 0)]
track_names = {}

scanner = None
track_mask = None
track_mask_draw = None

def tracker_init(size, headless):
    global scanner
    global track_mask, track_mask_draw
    global font

    scanner = zbar.ImageScanner()
    scanner.parse_config('enable')
    if not headless:
        track_mask = Image.new("RGBA", size, (255, 255, 255, 255))
        track_mask_draw = ImageDraw.Draw(track_mask)
        font = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationMono-Bold.ttf", 36)

def tracker_scan(pi, headless):
    global scanner
    global track_mask, track_mask_draw
    pil = pi.copy().convert('L')
    if not headless:
        color_image = pi.copy().convert('RGBA')
    width, height = pil.size
    raw = pil.tostring()

    # wrap image data
    image = zbar.Image(width, height, 'Y800', raw)

    # scan the image for barcodes
    scanner.scan(image)

    labels = {}

    if not headless:
        draw = ImageDraw.Draw(color_image)
    # extract results
    width = 4
        
    for symbol in image:

        w = math.sqrt((symbol.location[3][0] - symbol.location[0][0])**2+(symbol.location[3][1] - symbol.location[0][1])**2)
        h = math.sqrt((symbol.location[1][0] - symbol.location[0][0])**2+(symbol.location[1][1] - symbol.location[0][1])**2)

        x = symbol.location[3][0] - symbol.location[0][0]
        y = symbol.location[3][1] - symbol.location[0][1]

        angle = math.atan2(y, x)
        a = math.sqrt(w**2+h**2)/2
        cx = symbol.location[0][0] + a*math.cos(angle+math.pi/4)
        cy = symbol.location[0][1] + a*math.sin(angle+math.pi/4)


        if symbol.data in track_names:
            if not headless:
                track_mask_draw.line((track_names[symbol.data]["last_pt"], (cx, cy)), fill=track_names[symbol.data]["color"], width=width)

            track_names[symbol.data]["last_pt"] = (cx, cy)
        else:
            track_names[symbol.data] = {"last_pt": (cx, cy), "color": track_colors[len(track_names)] if len(track_names)<=len(track_colors) else (0,0,0)}

        if not headless:
            draw.line(symbol.location[:2], fill=(0, 255,0,255), width=width)
            draw.line(symbol.location[1:3], fill=(0, 255,0,255), width=width)
            draw.line(symbol.location[2:], fill=(0, 255,0,255), width=width)
            draw.line((symbol.location[0], symbol.location[-1]), fill=(0, 255,0,255), width=width)

            draw.arc((int(cx-2), int(cy-2), int(cx+2), int(cy+2)), 0, 360, fill=(255, 50, 50, 255))

            tsize = draw.textsize(symbol.data, font=font)
            draw.text((cx-tsize[0]/2, cy-tsize[1]/2), symbol.data, fill=(0,255,0,255), font=font)

        labels[symbol.data] = (cx, cy, angle)


    # color_image.putalpha(mask)
    # out_image = Image.blend(color_image, track_mask, 0.5)
    if not headless:
        out_image = Image.composite(color_image, track_mask, track_mask)
        del draw 

    # clean up
        del(image)
        del(color_image)
        del(pil)
        return out_image.convert("RGB"), labels
    return None, labels
