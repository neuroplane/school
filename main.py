import json
import os
import sys
import textwrap

import jmespath
import requests
import PIL
from PIL import Image, ImageDraw, ImageFont, ImageOps
from datetime import datetime, timezone, timedelta

##########################################################
###### WIKIPEDIA
wikiurl = "https://ru.wikipedia.org/w/api.php"
querystring = {"action": "query", "format":"json", "titles":"электрон","prop":"extracts","utf8":"true","redirects":"1","exintro":"","explaintext":""}

payload = ""
headers = {"cookie": "WMF-Last-Access=14-Aug-2021; WMF-Last-Access-Global=14-Aug-2021; GeoIP=RU%3ASE%3AVladikavkaz%3A43.03%3A44.67%3Av4"}

response = requests.request("GET", wikiurl, data=payload, headers=headers, params=querystring).json()
wotd = jmespath.search("query.pages.*.extract | [0]", response)
print(wotd)
H = 640
W = 384

COL1LEFT = 20
COL1RIGHT = W/2 - 20
COL1CENTER = W/4
COL2LEFT = W/2 + 20
COL2RIGHT = W - 20
CENTER = W/2
im = PIL.Image.new(mode="RGB", size=(384, 640), color=(255, 255, 255))
draw = ImageDraw.Draw(im)
###############################################
boston = ImageFont.truetype('fonts/nhlboston.ttf', 24)
robotocond = ImageFont.truetype('fonts/robotocond.ttf', 11)
mach = ImageFont.truetype('fonts/mach.otf', 40)
machsmall = ImageFont.truetype('fonts/mach.otf', 25)
machbig = ImageFont.truetype('fonts/mach.otf', 140)
unreal = ImageFont.truetype('fonts/unreal.ttf', 20)
ubuntu = ImageFont.truetype('fonts/Ubuntu-M.ttf', 65)
ubuntuс = ImageFont.truetype('fonts/ubuntuc.ttf', 16)
kroftsman = ImageFont.truetype('fonts/kroftsman.ttf', 150)
kroftsmansm = ImageFont.truetype('fonts/kroftsman.ttf', 150)
minecraftia = ImageFont.truetype('fonts/minecraftia.ttf', 8)
mario = ImageFont.truetype('fonts/mario.ttf', 8)
superstar = ImageFont.truetype('fonts/superstar.ttf', 16)
pixeled = ImageFont.truetype('fonts/pixeled.ttf',6)
dfont = mario
greyFont = (230, 230, 230, 128)
blackFont = (0, 0, 0)
LINESTART = 50
LINEHEIGHT = 20
draw.text((COL1CENTER, 30), "РАСПИСАНИЕ", font=dfont, fill=blackFont, anchor="mm")
draw.text((COL1LEFT, LINESTART + LINEHEIGHT*0), "09:00 Русский язык", font=dfont, fill=greyFont, anchor="lm")
draw.text((COL1LEFT, LINESTART + LINEHEIGHT*1), "10:00 Математика", font=dfont, fill=blackFont, anchor="lm")
draw.text((COL1LEFT, LINESTART + LINEHEIGHT*2), "10:40 Природоведение", font=dfont, fill=blackFont, anchor="lm")
draw.text((COL1LEFT, LINESTART + LINEHEIGHT*3), "13:00 Хоккей", font=dfont, fill=blackFont, anchor="lm")
# draw.text((COL1RIGHT, LINESTART), "COL1R", font=dfont, fill=greyFont, anchor="rm")
draw.text((COL2LEFT, LINESTART), "COL2L", font=dfont, fill=blackFont, anchor="lm")
draw.text((COL2RIGHT, LINESTART), "COL2R", font=dfont, fill=greyFont, anchor="rm")
index = 2
wotdline = 16
for line in textwrap.wrap(wotd, 65):
    draw.text((COL1LEFT, H/2 + wotdline*index), line, font=robotocond, fill=blackFont, anchor="lm")
    index = index + 1
# draw.line((CENTER, LINESTART, CENTER, H), fill=greyFont, width=1)
# This method will show image in any image viewer
im.show()
