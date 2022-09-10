#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os

libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')

if os.path.exists(libdir):
    sys.path.append(libdir)

print('libdir:', libdir)

import logging
from waveshare_epd import epd7in5_V2
import time
from PIL import Image,ImageDraw,ImageFont
import traceback


import imgkit
logging.info('creating image from website')

options = {
    'xvfb':'',
    'crop-h':480,
    'crop-w':800
}
imgkit.from_url('http://192.168.0.22:5000', os.path.join(picdir, 'out.bmp'), options=options)

print('start to try')

try:
    print("epd7in5_V2 Hack")

    epd = epd7in5_V2.EPD()
    print(epd)
    print("init and Clear")
    epd.init()
    epd.Clear()
    print("read bmp file")
    # Himage = Image.open('out.bmp')
    # epd.display(epd.getbuffer(Himage))

    Himage2 = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame
    bmp = Image.open(os.path.join(picdir, 'out.bmp'))
    epd.display(epd.getbuffer(bmp))

    print('image should be displayed')
    time.sleep(20)

    print("Clear...")
    epd.init()
    epd.Clear()

    print("Goto Sleep...")
    epd.sleep()

except IOError as e:
    print(e)

except KeyboardInterrupt:
    print("ctrl + c:")
    epd7in5.epdconfig.module_exit()
    exit()
