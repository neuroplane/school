#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os

picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
# fontdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'fonts')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_epd import epd7in5_V2
import time
from PIL import Image, ImageDraw, ImageFont
import traceback
import textwrap
import requests
from datetime import datetime, timezone, timedelta
import jmespath
import json

logging.basicConfig(level=logging.DEBUG)
######################################################################################################
### SCHEDULE
apiurl = "https://x125.ru/api/public/getdayschedule"
ozhegovapi = "https://x125.ru/api/public/randomozhegov"
homeworkapi = "https://x125.ru/api/public/gethomework"
payload = ""
headers = {
    "Content-Type": "application/json",
    "Authorization": "Token 11609376-ff57-401e-88a4-53f4c0904fdb"
}

schedule = requests.request("POST", apiurl, data=payload, headers=headers).json()
#print(schedule)

ozhegov = requests.request("POST", ozhegovapi, data=payload, headers=headers).json()
homework = requests.request("POST", homeworkapi, data=payload, headers=headers).json()

###### WIKIPEDIA
wikiurl = "https://ru.wikipedia.org/w/api.php"
querystring = {"action": "query", "format": "json", "titles": "электрон", "prop": "extracts", "utf8": "true",
               "redirects": "1", "exintro": "", "explaintext": ""}

payload = ""
headers = {
    "cookie": "WMF-Last-Access=14-Aug-2021; WMF-Last-Access-Global=14-Aug-2021; GeoIP=RU%3ASE%3AVladikavkaz%3A43.03%3A44.67%3Av4"}

response = requests.request("GET", wikiurl, data=payload, headers=headers, params=querystring).json()
wotd = jmespath.search("query.pages.*.extract | [0]", response)
#print(ozhegov)
epd = epd7in5_V2.EPD()
H = 800
W = epd.width

COL1LEFT = 20
COL1RIGHT = W / 2 - 20
COL1CENTER = W / 4
COL2LEFT = W / 2 + 20
COL2RIGHT = W - 20
CENTER = W / 2
#########################################################
thintel = ImageFont.truetype('../fonts/thintel.ttf', 18)
robotoc = ImageFont.truetype('../fonts/robotoc.ttf', 18)
robotoc20 = ImageFont.truetype('../fonts/robotoc.ttf', 20)
robotoc24 = ImageFont.truetype('../fonts/robotoc.ttf', 28)
freepixel = robotoc = ImageFont.truetype('../fonts/freepixel.ttf', 24)
nes = ImageFont.truetype('../fonts/1997.ttf', 12)
superstar = ImageFont.truetype('../fonts/superstar.ttf', 16)
basis = ImageFont.truetype('../fonts/basis33.ttf', 16)
dfont = basis
ozhegovfont = nes
greyFont = (128, 128, 128, 128)
blackFont = (0, 0, 0)
LINESTART = 0
LINEHEIGHT = 24
R1C1 = R1C2 = R2C1 = R2C2 = R3C1 = R3C2 = 1
textline = 17
######################################################################################################
try:
    logging.info("epd7in5_V2 Demo")
    # epd = epd7in5_V2.EPD()

    logging.info("init and Clear")
    epd.init()
    epd.Clear()

    # Drawing on the Vertical image
    logging.info("2.Drawing on the Vertical image...")
    Limage = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame
    draw = ImageDraw.Draw(Limage)
    #################################################################################################################
    # ROW 1 COLUMN 1
    for lesson in schedule:
        if int(lesson['time_to']) >= 0:
            overduegrey = "black"
        else:
            overduegrey = "black"
        draw.text((COL1LEFT, LINESTART + textline * R1C1), lesson['time'] + "   " + lesson['lesson_name'], font=dfont,
                  fill=overduegrey, anchor="lm")
        R1C1 = R1C1 + 1
    ########################################################################################
    # ROW 1 COLUMN 2
    ROW2 = H / 3
    for line in homework['homework'].splitlines():
        for alllines in textwrap.wrap(line, width=65):
            draw.text((COL1LEFT, ROW2 + textline * R2C1), alllines, font=dfont, fill="black", anchor="lm")
            R2C1 = R2C1 + 1
    # for line in textwrap.wrap("Математика: с. 24 (устно).Пропись: с.12-13. Азбука: с.19 (вспомнить и пересказать сказку), правило.", 25):
    #    draw.text((COL2LEFT, LINESTART + textline * R1C2), line, font=dfont, fill="black", anchor="lm")
    #    R1C2 = R1C2 + 1

    # ROW 2 COLUMN 1
    # shift = 50
    # for game in games:
    #    linehome = str(game['home'])
    #    lineaway = str(game['away'])
    #    if game['type'] is not None:
    #        type = str(game['type'])
    #        draw.text((COL1RIGHT-30, H / 3 + textline * R2C1), type, font=dfont, fill=0, anchor="rm")
    #    score = str(game['homescore']) + " : " + str(game['awayscore'])
    #    draw.text((COL1LEFT+shift, H/3 + textline*R2C1), linehome, font=dfont, fill=0, anchor="lm")
    #    draw.text((COL1RIGHT-shift, H / 3 + textline * R2C1), lineaway, font=dfont, fill=0, anchor="rm")
    #    draw.text((COL1CENTER, H / 3 + textline * R2C1), score, font=dfont, fill=0, anchor="mm")
    #    R2C1 = R2C1 + 1
    ROW3 = H / 3 * 2

    for definition in ozhegov:

        draw.text((COL1LEFT, ROW3 + textline * R3C1), definition['vocab'], font=ozhegovfont, fill="black", anchor="lm")
        R3C1 = R3C1 + 1
        R3C2 = R3C2 + 1
        for line in textwrap.wrap(definition['def'], width=60):
            draw.text((COL1LEFT, ROW3 + textline * R3C1), line, font=dfont, fill="black", anchor="lm")
            R3C1 = R3C1 + 1
        if definition['leglexam'] != None:
            for line in textwrap.wrap(definition['leglexam'], width=60):
                draw.text((COL1LEFT, ROW3 + textline * (R3C1)), "||  " + line, font=dfont, fill="black", anchor="lm")
                R3C1 = R3C1 + 1
        R3C1 = R3C1 + 1
    #######
    # draw.text((COL1LEFT, H/2 + textline * R2C1), ozhegov['vocab'], font=dfont, fill="black", anchor="lm")
    # draw.text((COL1LEFT, H/2 + textline * (R2C1+2)), ozhegov['def'], font=dfont, fill="black", anchor="lm")
    ################################################################################################################
    epd.display(epd.getbuffer(Limage))
    # time.sleep(2)


    logging.info("Goto Sleep...")
    epd.sleep()

except IOError as e:
    logging.info(e)

except KeyboardInterrupt:
    logging.info("ctrl + c:")
    epd7in5_V2.epdconfig.module_exit()
    exit()