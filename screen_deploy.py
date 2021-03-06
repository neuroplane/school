#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os

picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
fontsdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'fonts')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_epd import epd5in83
import time
from PIL import Image, ImageDraw, ImageFont
import traceback

import requests
import textwrap
import jmespath
import datetime
from datetime import datetime, timezone, timedelta

logging.basicConfig(level=logging.DEBUG)
#################################################
### SCHEDULE
apiurl = "https://x125.ru/api/public/getdayschedule"

payload = ""
headers = {
    "Content-Type": "application/json",
    "Authorization": "Token 11609376-ff57-401e-88a4-53f4c0904fdb"
}

schedule = requests.request("POST", apiurl, data=payload, headers=headers).json()
print(schedule)

###### WIKIPEDIA
wikiurl = "https://ru.wikipedia.org/w/api.php"
querystring = {"action": "query", "format": "json", "titles": "электрон", "prop": "extracts", "utf8": "true",
               "redirects": "1", "exintro": "", "explaintext": ""}

payload = ""
headers = {
    "cookie": "WMF-Last-Access=14-Aug-2021; WMF-Last-Access-Global=14-Aug-2021; GeoIP=RU%3ASE%3AVladikavkaz%3A43.03%3A44.67%3Av4"}

response = requests.request("GET", wikiurl, data=payload, headers=headers, params=querystring).json()
wotd = jmespath.search("query.pages.*.extract | [0]", response)
print(wotd)
H = 600
W = 448

COL1LEFT = 20
COL1RIGHT = W / 2 - 20
COL1CENTER = W / 4
COL2LEFT = W / 2 + 20
COL2RIGHT = W - 20
CENTER = W / 2

thintel = ImageFont.truetype('../fonts/thintel.ttf', 16)
dfont = thintel
greyFont = (128, 128, 128, 128)
blackFont = (0, 0, 0)
LINESTART = 30
LINEHEIGHT = 20
R1C1 = R1C2 = R2C1 = R2C2 = R3C1 = R3C2 = 2
studies = [{"time": "08:30", "name": "Русский язык", "overdue": True},
           {"time": "09:30", "name": "Литературное чтение", "overdue": True},
           {"time": "10:30", "name": "Осетинский язык", "overdue": True},
           {"time": "11:30", "name": "ИЗО", "overdue": False},
           {"time": "13:10", "name": "Ледовая тренировка", "overdue": False},
           {"time": "16:00", "name": "Бросковая", "overdue": False}]
games = [{"home": "TBL", "away": "CAR", "homescore": "4", "awayscore": "3", "type": "OT"},
         {"home": "CBJ", "away": "WSH", "homescore": "3", "awayscore": "5", "type": "SO"},
         {"home": "NSH", "away": "MIN", "homescore": "2", "awayscore": "5", "type": ""},
         {"home": "TBL", "away": "CAR", "homescore": "4", "awayscore": "3", "type": "OT"},
         {"home": "CBJ", "away": "WSH", "homescore": "3", "awayscore": "5", "type": "SO"},
         {"home": "NSH", "away": "MIN", "homescore": "2", "awayscore": "5", "type": ""},
         {"home": "TBL", "away": "CAR", "homescore": "4", "awayscore": "3", "type": "OT"},
         {"home": "CBJ", "away": "WSH", "homescore": "3", "awayscore": "5", "type": "SO"},
         {"home": "NSH", "away": "MIN", "homescore": "2", "awayscore": "5", "type": ""}]
standings = [{"name": "Tampa Bay Lightning", "points": "35"}, {"name": "Minnesota Wild", "points": "33"},
             {"name": "Washington Capitals", "points": "32"}, {"name": "Boston Bruins", "points": "31"},
             {"name": "Columbus Blue Jackets", "points": "29"}, {"name": "Washington Capitals", "points": "32"},
             {"name": "Boston Bruins", "points": "31"}, {"name": "Columbus Blue Jackets", "points": "29"}]
fieldplayers = [{"name": "Kirill Kaprizov", "passes": "39", "goals": "29", "points": "58"},
                {"name": "Connor McDavid", "passes": "39", "goals": "29", "points": "58"},
                {"name": "Artemiy Panarin", "passes": "39", "goals": "29", "points": "58"},
                {"name": "Alex Ovechkin", "passes": "39", "goals": "29", "points": "58"},
                {"name": "David Pastrnak", "passes": "39", "goals": "29", "points": "58"},
                {"name": "Matt Barzal", "passes": "39", "goals": "29", "points": "58"},
                {"name": "Nikita Kucherov", "passes": "39", "goals": "29", "points": "58"}]
goalies = [{"name": "Andrei Vasilevskiy", "sv": ".925", "gaa": "2.21"},
           {"name": "Connor Hellebuyck", "sv": ".925", "gaa": "2.21"},
           {"name": "Jordan Binnington", "sv": ".925", "gaa": "2.21"},
           {"name": "Philipp Grubauer", "sv": ".925", "gaa": "2.21"},
           {"name": "Tristan Jarry", "sv": ".925", "gaa": "2.21"},
           {"name": "Marc-Andre Fleury", "sv": ".925", "gaa": "2.21"},
           {"name": "Semyon Varlamov", "sv": ".925", "gaa": "2.21"}]

index1 = 2
textline = 16
################################################
try:
    logging.info("epd5in83 Demo")

    epd = epd5in83.EPD()
    logging.info("init and Clear")
    epd.init()
    epd.Clear()

    font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
    font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)

    logging.info("Clear...")
    epd.init()
    epd.Clear()
    # ROW 1 COLUMN 1
    for lesson in schedule:
        if int(lesson['time_to']) >= 0:
            overduegrey = greyFont
        else:
            overduegrey = blackFont
        draw.text((COL1LEFT, LINESTART + textline * R1C1), lesson['time'] + "   " + lesson['lesson_name'], font=dfont, fill=overduegrey, anchor="lm")
        R1C1 = R1C1 + 1

    # ROW 1 COLUMN 2
    for line in textwrap.wrap("Математика: с. 24 (устно).Пропись: с.12-13. Азбука: с.19 (вспомнить и пересказать сказку), правило.", 40):
        draw.text((COL2LEFT, LINESTART + textline * R1C2), line, font=dfont, fill=blackFont, anchor="lm")
        R1C2 = R1C2 + 1

    #ROW 2 COLUMN 1
    shift = 50
    for game in games:
        linehome = str(game['home'])
        lineaway = str(game['away'])
        if game['type'] is not None:
            type = str(game['type'])
            draw.text((COL1RIGHT-30, H / 3 + textline * R2C1), type, font=dfont, fill=greyFont, anchor="rm")
        score = str(game['homescore']) + " : " + str(game['awayscore'])
        draw.text((COL1LEFT+shift, H/3 + textline*R2C1), linehome, font=dfont, fill=blackFont, anchor="lm")
        draw.text((COL1RIGHT-shift, H / 3 + textline * R2C1), lineaway, font=dfont, fill=blackFont, anchor="rm")
        draw.text((COL1CENTER, H / 3 + textline * R2C1), score, font=dfont, fill=blackFont, anchor="mm")
        R2C1 = R2C1 + 1

    #ROW 2 COLUMN 2
    for team in standings:
        teamname = str(team['name'])
        points = str(team['points'])
        draw.text((COL2LEFT, H / 3 + textline * R2C2), teamname, font=dfont, fill=blackFont, anchor="lm")
        draw.text((COL2RIGHT, H / 3 + textline * R2C2), points, font=dfont, fill=blackFont, anchor="rm")
        R2C2 = R2C2 + 1


    #ROW 3 COLUMN 1
    draw.text((COL1LEFT, H/3*2 + textline*R3C1), "Field player name", font=dfont, fill=blackFont, anchor="lm")
    draw.text((COL1RIGHT, H/3*2 + textline * R3C1), "P", font=dfont, fill=blackFont, anchor="rm")
    draw.text((COL1RIGHT-25, H / 3 * 2 + textline * R3C1), "G", font=dfont, fill=blackFont, anchor="rm")
    draw.text((COL1RIGHT - 50, H / 3 * 2 + textline * R3C1), "P", font=dfont, fill=blackFont, anchor="rm")
    draw.line((COL1LEFT, H/3*2+textline*(R3C1+1), COL1RIGHT, H/3*2+textline*(R3C1+1)), fill=greyFont)
    R3C1 = R3C1 + 2
    for player in fieldplayers:
        draw.text((COL1LEFT, H/3*2 + textline*R3C1), player['name'], font=dfont, fill=blackFont, anchor="lm")
        draw.text((COL1RIGHT, H/3*2 + textline * R3C1), player['points'], font=dfont, fill=blackFont, anchor="rm")
        draw.text((COL1RIGHT-25, H / 3 * 2 + textline * R3C1), player['goals'], font=dfont, fill=blackFont, anchor="rm")
        draw.text((COL1RIGHT - 50, H / 3 * 2 + textline * R3C1), player['passes'], font=dfont, fill=blackFont, anchor="rm")

        R3C1 = R3C1 + 1

    #ROW 3 COLUMN2

    draw.text((COL2LEFT, H/3*2 + textline*R3C2), "Goalie name", font=dfont, fill=blackFont, anchor="lm")
    draw.text((COL2RIGHT, H/3*2 + textline * R3C2), "GAA", font=dfont, fill=blackFont, anchor="rm")
    draw.text((COL2RIGHT-35, H / 3 * 2 + textline * R3C2), "SV", font=dfont, fill=blackFont, anchor="rm")
    #draw.text((COL2RIGHT - 50, H / 3 * 2 + textline * R3C2), "P", font=thintel, fill=blackFont, anchor="rm")
    draw.line((COL2LEFT, H/3*2+textline*(R3C2+1), COL2RIGHT, H/3*2+textline*(R3C2+1)), fill=greyFont)
    R3C2 = R3C2 + 2
    for goalie in goalies:
        draw.text((COL2LEFT, H/3*2 + textline*R3C2), goalie['name'], font=dfont, fill=blackFont, anchor="lm")
        draw.text((COL2RIGHT, H/3*2 + textline * R3C2), goalie['gaa'], font=dfont, fill=blackFont, anchor="rm")
        draw.text((COL2RIGHT-35, H / 3 * 2 + textline * R3C2), goalie['sv'], font=dfont, fill=blackFont, anchor="rm")
        #draw.text((COL2RIGHT - 50, H / 3 * 2 + textline * R3C2), goalie['passes'], font=thintel, fill=blackFont, anchor="rm")

        R3C2 = R3C2 + 1
    index = 2
    textline = 16
    draw.line((COL1LEFT-10, H/3, COL2RIGHT+10, H/3), fill=greyFont)
    draw.line((COL1LEFT-10, H/3*2, COL2RIGHT+10, H/3*2), fill=greyFont)
logging.info("Goto Sleep...")
epd.sleep()

except IOError as e:
logging.info(e)

except KeyboardInterrupt:
logging.info("ctrl + c:")
epd5in83.epdconfig.module_exit()
exit()