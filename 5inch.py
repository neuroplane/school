import json
import os
import sys
import textwrap
from time import strptime, strftime, time

import lipsum

import jmespath
import requests
import PIL
from PIL import Image, ImageDraw, ImageFont, ImageOps
import datetime
from datetime import datetime, timezone, timedelta

##########################################################
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
ozhegov = requests.request("POST", ozhegovapi, data=payload, headers=headers).json()
homework = requests.request("POST", homeworkapi, data=payload, headers=headers).json()
#print((homework['homework'].splitlines()))
###### WIKIPEDIA
wikiurl = "https://ru.wikipedia.org/w/api.php"
querystring = {"action": "query", "format":"json", "titles":"электрон","prop":"extracts","utf8":"true","redirects":"1","exintro":"","explaintext":""}

payload = ""
headers = {"cookie": "WMF-Last-Access=14-Aug-2021; WMF-Last-Access-Global=14-Aug-2021; GeoIP=RU%3ASE%3AVladikavkaz%3A43.03%3A44.67%3Av4"}

response = requests.request("GET", wikiurl, data=payload, headers=headers, params=querystring).json()
wotd = jmespath.search("query.pages.*.extract | [0]", response)
#print(wotd)
H = 800
W = 480

COL1LEFT = 20
COL1RIGHT = W/2 - 20
COL1CENTER = W/4
COL2LEFT = W/2 + 20
COL2RIGHT = W - 20
CENTER = W/2
im = PIL.Image.new(mode="RGB", size=(448, 600), color=(255, 255, 255))
draw = ImageDraw.Draw(im)
###############################################
boston = ImageFont.truetype('fonts/nhlboston.ttf', 24)
robotocond = ImageFont.truetype('fonts/robotocond.ttf', 16)
mach = ImageFont.truetype('fonts/mach.otf', 40)
machsmall = ImageFont.truetype('fonts/mach.otf', 25)
machbig = ImageFont.truetype('fonts/mach.otf', 140)
unreal = ImageFont.truetype('fonts/unreal.ttf', 14)
ubuntu = ImageFont.truetype('fonts/Ubuntu-M.ttf', 16)
ubuntuc = ImageFont.truetype('fonts/ubuntuc.ttf', 16)
kroftsman = ImageFont.truetype('fonts/kroftsman.ttf', 150)
kroftsmansm = ImageFont.truetype('fonts/kroftsman.ttf', 20)
minecraftia = ImageFont.truetype('fonts/minecraftia.ttf', 8)
thintel = ImageFont.truetype('fonts/thintel.ttf', 16)
superstar = ImageFont.truetype('fonts/superstar.ttf', 16)
pixeled = ImageFont.truetype('fonts/pixeled.ttf',10)
mario = ImageFont.truetype('fonts/mario.ttf',16)
pixel7 = ImageFont.truetype('fonts/pixel7.ttf',14)
basis = ImageFont.truetype('fonts/basis33.ttf',16)
dfont = basis
ozhegovfont = superstar
greyFont = (128, 128, 128, 128)
greyfill = 128
blackFont = (0, 0, 0)
LINESTART = 0
LINEHEIGHT = 38

R1C1 = R1C2 = R2C1 = R2C2 = R3C1 = R3C2 = 2
studies = [{"time":"08:30","name":"Русский язык","overdue": True},{"time":"09:30","name":"Литературное чтение","overdue":True},{"time":"10:30","name":"Осетинский язык","overdue":True},{"time":"11:30","name":"ИЗО","overdue":False},{"time":"13:10","name":"Ледовая тренировка","overdue":False},{"time":"16:00","name":"Бросковая","overdue":False}]
games = [{"home":"TBL","away":"CAR","homescore":"4","awayscore":"3","type":"OT"},{"home":"CBJ","away":"WSH","homescore":"3","awayscore":"5","type":"SO"},{"home":"NSH","away":"MIN","homescore":"2","awayscore":"5","type":""},{"home":"TBL","away":"CAR","homescore":"4","awayscore":"3","type":"OT"},{"home":"CBJ","away":"WSH","homescore":"3","awayscore":"5","type":"SO"},{"home":"NSH","away":"MIN","homescore":"2","awayscore":"5","type":""},{"home":"TBL","away":"CAR","homescore":"4","awayscore":"3","type":"OT"},{"home":"CBJ","away":"WSH","homescore":"3","awayscore":"5","type":"SO"},{"home":"NSH","away":"MIN","homescore":"2","awayscore":"5","type":""}]
standings = [{"name":"Tampa Bay Lightning","points":"35"},{"name":"Minnesota Wild","points":"33"},{"name":"Washington Capitals","points":"32"},{"name":"Boston Bruins","points":"31"},{"name":"Columbus Blue Jackets","points":"29"},{"name":"Washington Capitals","points":"32"},{"name":"Boston Bruins","points":"31"},{"name":"Columbus Blue Jackets","points":"29"}]
fieldplayers = [{"name":"Kirill Kaprizov","passes":"39","goals":"29","points":"58"},{"name":"Connor McDavid","passes":"39","goals":"29","points":"58"},{"name":"Artemiy Panarin","passes":"39","goals":"29","points":"58"},{"name":"Alex Ovechkin","passes":"39","goals":"29","points":"58"},{"name":"David Pastrnak","passes":"39","goals":"29","points":"58"},{"name":"Matt Barzal","passes":"39","goals":"29","points":"58"},{"name":"Nikita Kucherov","passes":"39","goals":"29","points":"58"}]
goalies = [{"name":"Andrei Vasilevskiy","sv":".925","gaa":"2.21"},{"name":"Connor Hellebuyck","sv":".925","gaa":"2.21"},{"name":"Jordan Binnington","sv":".925","gaa":"2.21"},{"name":"Philipp Grubauer","sv":".925","gaa":"2.21"},{"name":"Tristan Jarry","sv":".925","gaa":"2.21"},{"name":"Marc-Andre Fleury","sv":".925","gaa":"2.21"},{"name":"Semyon Varlamov","sv":".925","gaa":"2.21"}]
goalies = []

index1 = 2
textline = 18
# ROW 1 COLUMN 1
for lesson in schedule:
    if int(lesson['time_to']) >= 0:
        overduegrey = "grey"
    else:
        overduegrey = "black"
    draw.text((COL1LEFT, LINESTART + textline * R1C1), lesson['time'] + " " + lesson['lesson_name'], font=dfont, fill=overduegrey, anchor="lm")

    R1C1 = R1C1 + 1

# ROW 1 COLUMN 2
# R1C2 = R1C2 + 1

#ROW 2 COLUMN 1
ROW2 = H/3-40
for line in homework['homework'].splitlines():
    for alllines in textwrap.wrap(line, width=55):
        draw.text((COL1LEFT, ROW2 + textline * R2C1), alllines, font=dfont, fill=blackFont, anchor="lm")
        R2C1 = R2C1 + 1

#ROW 2 COLUMN 2

#for team in standings:
#R2C2 = R2C2 + 1


#ROW 3 COLUMN 1
ROW3 = H/3 * 2 - 30
for definition in ozhegov:

    draw.text((COL1LEFT, ROW3 + textline * R3C1), definition['vocab'], font=ozhegovfont, fill=blackFont, anchor="lm")
    R3C1 = R3C1 + 1
    R3C2 = R3C2 + 1
    for line in textwrap.wrap(definition['def'], width=55):
        draw.text((COL1LEFT, ROW3 + textline * R3C1), line, font=dfont, fill=blackFont, anchor="lm")
        R3C1 = R3C1 + 1
    if definition['leglexam'] != None:
        for line in textwrap.wrap(definition['leglexam'], width=55):
            draw.text((COL1LEFT, ROW3 + textline * (R3C1)), "||  " +  line, font=dfont, fill=blackFont, anchor="lm")
            R3C1 = R3C1 + 1
    R3C1 = R3C1 + 1

#draw.text((COL1LEFT, H/3*2 + textline*R3C1), ozhegov['vocab'], font=ozhegovfont, fill=blackFont, anchor="lm")
#for line in textwrap.wrap(ozhegov['def'], 30):
#    draw.text((COL1LEFT, H/3*2 + textline*(R3C1+2)), line, font=dfont, fill=blackFont, anchor="lm")
#    R3C1 = R3C1 + 1
#if ozhegov['leglexam'] != None:
#    for leglexam in textwrap.wrap(ozhegov['leglexam'], 27):
#        draw.text((COL2LEFT, H/3*2 + textline*(R3C2+2)), leglexam, font=dfont, fill=blackFont, anchor="lm")
#        R3C2 = R3C2 + 1
#    R3C1 = R3C1 + 1

#ROW 3 COLUMN2
#    R3C2 = R3C2 + 1
index = 2
textline = 16
draw.line((COL1LEFT-10, ROW2, COL2RIGHT+10, ROW2), fill=greyFont)
draw.line((COL1LEFT-10, ROW3, COL2RIGHT+10, ROW3), fill=greyFont)


#draw.line((CENTER, LINESTART, CENTER, H), fill=greyFont, width=1)
# This method will show image in any image viewer
im.show()
