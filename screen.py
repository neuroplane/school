#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os

picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_epd import epd5in83
import time
from PIL import Image, ImageDraw, ImageFont, ImageOps
import traceback

import requests
from datetime import datetime, timezone, timedelta
import jmespath
import json

##########################################################
now = datetime.today().strftime('%H:%M:%S')
yesterday = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')
yesterday_rus = (datetime.today() - timedelta(days=1)).strftime('%d.%m.%Y')
##########################################################
last_games = requests.get(
    "https://statsapi.web.nhl.com/api/v1/schedule?startDate=" + yesterday + "&endDate=" + yesterday + "&hydrate=team,linescore,broadcasts(all),tickets,game(content(media(epg)),seriesSummary),radioBroadcasts,metadata,seriesSummary(series)&site=ru_nhl&teamId=&gameType=&timecode=").json()
last_games_parsed = jmespath.search(
    "dates[].games[].teams[].{away: {team: away.team.teamName, loc: away.team.locationName, score: away.score},home:{team: home.team.teamName, loc: home.team.locationName, score: home.score}}",
    last_games)

########### BEST BOMBARDIERS
field_players = requests.get(
    "https://api.nhle.com/stats/rest/ru/skater/summary?isAggregate=false&isGame=false&sort=%5B%7B%22property%22:%22points%22,%22direction%22:%22DESC%22%7D,%7B%22property%22:%22goals%22,%22direction%22:%22DESC%22%7D,%7B%22property%22:%22assists%22,%22direction%22:%22DESC%22%7D%5D&start=0&limit=50&factCayenneExp=gamesPlayed%3E=1&cayenneExp=gameTypeId=2%20and%20seasonId%3C=20202021%20and%20seasonId%3E=20202021").json()
field_players_parsed = jmespath.search(
    "data[].{name: skaterFullName, team: teamAbbrevs, position: positionCode, goals: goals, assists: assists, points: points, plusminus: plusMinus}",
    field_players)

########### GOALIES
goalies = requests.get(
    "https://api.nhle.com/stats/rest/ru/goalie/summary?isAggregate=false&isGame=false&sort=%5B%7B%22property%22:%22wins%22,%22direction%22:%22DESC%22%7D,%7B%22property%22:%22savePct%22,%22direction%22:%22DESC%22%7D%5D&start=0&limit=50&factCayenneExp=gamesPlayed%3E=1&cayenneExp=gameTypeId=2%20and%20seasonId%3C=20202021%20and%20seasonId%3E=20202021").json()
goalies_parsed = jmespath.search(
    "data[].{goalie: goalieFullName, team: teamAbbrevs, gaa: goalsAgainstAverage, shutouts: shutouts, saves: savePct, wins: wins}",
    goalies)
###########################################################
logging.basicConfig(level=logging.DEBUG)

try:

    epd = epd5in83.EPD()
    epd.init()
    epd.Clear()

    font_thintel = ImageFont.truetype(os.path.join(picdir, 'thintel.ttf'), 16)
    font_machinec = ImageFont.truetype(os.path.join(picdir, 'machinec.otf'), 48)
    font_upheaval = ImageFont.truetype(os.path.join(picdir, 'upheaval.ttf'), 20)

    SCW = epd.height
    SCH = epd.width
    def_font = font_thintel
    START_Y_SCORES = 50
    LINE_HEIGHT = 12
    Limage = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame
    draw = ImageDraw.Draw(Limage)

    # draw.text((2, 0), 'hello world and many others', font = font_thintel, fill = 0)
    # draw.text((2, 20), str(epd.height) , font = font18, fill = 0)
    ##### GAMES DRAW
    draw.text((3, 3), now, font=font_thintel, fill=0)
    draw.text((SCW / 2, 20), 'ПОСЛЕДНИЕ ИГРЫ ' + str(yesterday_rus) + '', font=font_upheaval, fill=0, anchor="mm")
    draw.line((10, LINE_HEIGHT + 20, SCW - 10, LINE_HEIGHT + 20), fill=0, width=1)
    for item in last_games_parsed:
        line_away = str.upper(item['away']['loc']) + "   " + str.upper(item['away']['team'])
        line_score = str(item['away']['score']) + " : " + str(item['home']['score'])
        line_home = str.upper(item['home']['loc']) + "   " + str.upper(item['home']['team'])
        # print(w)
        # draw.rectangle((START_X,START_Y, 11, 11), fill = 0)
        draw.text((SCW / 2 - 30, START_Y_SCORES), line_away, font=def_font, fill=0, anchor="rm")
        draw.text((SCW / 2, START_Y_SCORES), line_score, font=def_font, fill=0, anchor="mm")
        draw.text((SCW / 2 + 30, START_Y_SCORES), line_home, font=def_font, fill=0, anchor="lm")
        START_Y_SCORES = START_Y_SCORES + LINE_HEIGHT
    #################################################################################################################
    ###### FIELD PLAYERS DRAW
    START_Y_FIELDPLAYERS = START_Y_SCORES + 20
    draw.text((SCW / 2, START_Y_FIELDPLAYERS), 'БОМБАРДИРЫ', font=font_upheaval, fill=0, anchor="mm")
    draw.line((10, LINE_HEIGHT + START_Y_FIELDPLAYERS, SCW - 10, LINE_HEIGHT + START_Y_FIELDPLAYERS), fill=0, width=1)
    START_Y_FIELDPLAYERS = START_Y_FIELDPLAYERS + LINE_HEIGHT * 2
    pos_num = 25
    pos_name = pos_num + 15
    pos_team = pos_name + 120  # 130
    pos_position = pos_team + 35  # 155
    pos_goals = pos_position + 45  # 180
    pos_assists = pos_goals + 35  # 210
    pos_points = pos_assists + 35  # 240
    pos_plusminus = pos_points + 35  # 270

    draw.text((pos_num, START_Y_FIELDPLAYERS), '#', font=def_font, fill=0, anchor="rm")
    draw.text((pos_name, START_Y_FIELDPLAYERS), "ИМЯ", font=def_font, fill=0, anchor="lm")
    draw.text((pos_team, START_Y_FIELDPLAYERS), "КОМ", font=def_font, fill=0, anchor="lm")
    draw.text((pos_position, START_Y_FIELDPLAYERS), "ПОЗ", font=def_font, fill=0, anchor="lm")
    draw.text((pos_goals, START_Y_FIELDPLAYERS), "ГОЛ", font=def_font, fill=0, anchor="rm")
    draw.text((pos_assists, START_Y_FIELDPLAYERS), "ПАС", font=def_font, fill=0, anchor="rm")
    draw.text((pos_points, START_Y_FIELDPLAYERS), "ОЧК", font=def_font, fill=0, anchor="rm")
    draw.text((pos_plusminus, START_Y_FIELDPLAYERS), "+/-", font=def_font, fill=0, anchor="rm")
    draw.line((10, START_Y_FIELDPLAYERS + LINE_HEIGHT, SCW - 10, START_Y_FIELDPLAYERS + LINE_HEIGHT), fill=0, width=1)
    START_Y_FIELDPLAYERS = START_Y_FIELDPLAYERS + LINE_HEIGHT * 2
    for index, item in zip(range(10), field_players_parsed):
        draw.text((pos_num, START_Y_FIELDPLAYERS), str(index + 1), font=def_font, fill=0, anchor="rm")
        draw.text((pos_name, START_Y_FIELDPLAYERS), item['name'], font=def_font, fill=0, anchor="lm")
        draw.text((pos_team, START_Y_FIELDPLAYERS), item['team'], font=def_font, fill=0, anchor="lm")
        draw.text((pos_position, START_Y_FIELDPLAYERS), item['position'], font=def_font, fill=0, anchor="lm")
        draw.text((pos_goals, START_Y_FIELDPLAYERS), str(item['goals']), font=def_font, fill=0, anchor="rm")
        draw.text((pos_assists, START_Y_FIELDPLAYERS), str(item['assists']), font=def_font, fill=0, anchor="rm")
        draw.text((pos_points, START_Y_FIELDPLAYERS), str(item['points']), font=def_font, fill=0, anchor="rm")
        draw.text((pos_plusminus, START_Y_FIELDPLAYERS), str(item['plusminus']), font=def_font, fill=0, anchor="rm")
        START_Y_FIELDPLAYERS = START_Y_FIELDPLAYERS + LINE_HEIGHT
    #################################################################################################################
    START_Y_GOALIES = START_Y_FIELDPLAYERS + 15
    draw.text((SCW / 2, START_Y_GOALIES), 'ВРАТАРИ', font=font_upheaval, fill=0, anchor="mm")
    draw.line((10, LINE_HEIGHT + START_Y_GOALIES, SCW - 10, LINE_HEIGHT + START_Y_GOALIES), fill=0, width=1)
    START_Y_GOALIES = START_Y_GOALIES + LINE_HEIGHT * 2
    pos_num = 25
    pos_name = pos_num + 15
    pos_saves = pos_team + 70
    pos_wins = pos_saves + 40
    pos_shutouts = pos_wins + 30
    pos_gaa = pos_shutouts + 50

    draw.text((pos_num, START_Y_GOALIES), '#', font=def_font, fill=0, anchor="rm")
    draw.text((pos_name, START_Y_GOALIES), "ИМЯ", font=def_font, fill=0, anchor="lm")
    draw.text((pos_team, START_Y_GOALIES), "КОМ", font=def_font, fill=0, anchor="lm")
    draw.text((pos_saves, START_Y_GOALIES), "СЭЙВЫ, %", font=def_font, fill=0, anchor="rm")
    draw.text((pos_wins, START_Y_GOALIES), "ПОБЕД", font=def_font, fill=0, anchor="rm")
    draw.text((pos_shutouts, START_Y_GOALIES), "СУХ", font=def_font, fill=0, anchor="rm")
    draw.text((pos_gaa, START_Y_GOALIES), "К. НАДЁЖ.", font=def_font, fill=0, anchor="rm")
    draw.line((10, START_Y_GOALIES + LINE_HEIGHT, SCW - 10, START_Y_GOALIES + LINE_HEIGHT), fill=0, width=1)
    START_Y_GOALIES = START_Y_GOALIES + LINE_HEIGHT * 2
    for index, item in zip(range(10), goalies_parsed):
        draw.text((pos_num, START_Y_GOALIES), str(index + 1), font=def_font, fill=0, anchor="rm")
        draw.text((pos_name, START_Y_GOALIES), item['goalie'], font=def_font, fill=0, anchor="lm")
        draw.text((pos_team, START_Y_GOALIES), item['team'], font=def_font, fill=0, anchor="lm")
        draw.text((pos_saves, START_Y_GOALIES), str(round(item['saves'] * 100, 1)), font=def_font, fill=0, anchor="rm")
        draw.text((pos_wins, START_Y_GOALIES), str(item['wins']), font=def_font, fill=0, anchor="rm")
        draw.text((pos_shutouts, START_Y_GOALIES), str(item['shutouts']), font=def_font, fill=0, anchor="rm")
        draw.text((pos_gaa, START_Y_GOALIES), str(round(item['gaa'], 3)), font=def_font, fill=0, anchor="rm")

        START_Y_GOALIES = START_Y_GOALIES + LINE_HEIGHT
    draw.text((SCW / 2, START_Y_GOALIES + LINE_HEIGHT * 4), '#ХОККЕЙВСЕРДЦЕ', font=font_machinec, fill=0, anchor="mm")
    print(START_Y_GOALIES)
    ################################################################################################################

    epd.display(epd.getbuffer(Limage))
    time.sleep(2)

    logging.info("Clear...")
    # epd.init()
    # epd.Clear()

    logging.info("Goto Sleep...")
    epd.sleep()

except IOError as e:
    logging.info(e)

except KeyboardInterrupt:
    logging.info("ctrl + c:")
    epd7in5.epdconfig.module_exit()
    exit()