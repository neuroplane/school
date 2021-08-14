import json
import os
import sys

import jmespath
import requests
import PIL
from PIL import Image, ImageDraw, ImageFont, ImageOps
from datetime import datetime, timezone, timedelta

##########################################################

JGtoken = "pt0xh1e0nu1o8seqcgtxnlen2v9ye6htugzna55u"
jsonObj = '[{"uid":"871f7d17-db4d-4863-8391-68113775d978","date":"December 14, 2021","name":"Lorie","country":"Tuvalu","lastname":"Hubbard"},{"uid":"ef444518-7d16-4732-9eaf-68abb6bc817e","date":"November 27, 2021","name":"Branch","country":"Bahrain","lastname":"Woodward"},{"uid":"b165968c-487d-4d29-bb34-6ec1ca21038b","date":"November 13, 2021","name":"Susan","country":"Lithuania","lastname":"Bright"},{"uid":"3613c0a6-f0f4-4104-8411-e1716239f502","date":"September 17, 2021","name":"Baxter","country":"Mauritania","lastname":"Matthews"},{"uid":"120fd700-9bd0-4a4e-8878-14fd83dcc7da","date":"October 8, 2021","name":"Adrian","country":"New Zealand","lastname":"Gomez"},{"uid":"128c4721-9dd4-4230-b52c-105c4ea089a1","date":"November 21, 2021","name":"Welch","country":"Sri Lanka","lastname":"Pollard"}]'
print(jsonObj)

H = 640
W = 384
COL1LEFT = 20
COL1RIGHT = W/2 - 20
COL2LEFT = W/2 + 20
COL2RIGHT = W - 20
CENTER = W/2
im = PIL.Image.new(mode="RGB", size=(384, 640), color=(255, 255, 255))
draw = ImageDraw.Draw(im)
###############################################
boston = ImageFont.truetype('fonts/nhlboston.ttf', 24)
robotocond = ImageFont.truetype('fonts/robotocond.ttf', 16)
mach = ImageFont.truetype('fonts/mach.otf', 40)
machsmall = ImageFont.truetype('fonts/mach.otf', 25)
machbig = ImageFont.truetype('fonts/mach.otf', 140)
unreal = ImageFont.truetype('fonts/unreal.ttf', 20)
ubuntu = ImageFont.truetype('fonts/Ubuntu-M.ttf', 65)
ubuntuс = ImageFont.truetype('fonts/ubuntuc.ttf', 65)
kroftsman = ImageFont.truetype('fonts/kroftsman.ttf', 150)
kroftsmansm = ImageFont.truetype('fonts/kroftsman.ttf', 150)
dfont = ubuntuс
greyFont = (230, 230, 230, 128)
blackFont = (0, 0, 0)
draw.text((CENTER, 10), "РАСПИСАНИЕ", font=dfont, fill=greyFont, anchor="mm")
draw.text((COL1LEFT, 50), "COL1", font=dfont, fill=blackFont, anchor="mm")
draw.text((COL1RIGHT, 50), "COL2", font=dfont, fill=greyFont, anchor="mm")
# This method will show image in any image viewer
im.show()
