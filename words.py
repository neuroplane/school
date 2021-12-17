import json
import os
import sys
import textwrap

import jmespath
import requests
import PIL
from PIL import Image, ImageDraw, ImageFont, ImageOps
from datetime import datetime, timezone, timedelta

###### WIKIPEDIA

#########################################################
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
boldfont52 = ImageFont.truetype('fonts/charisbold.ttf', 52)
font52 = ImageFont.truetype('fonts/charis.ttf', 52)
font44 = ImageFont.truetype('fonts/charis.ttf', 44)
font32 = ImageFont.truetype('fonts/charis.ttf', 32)
greyFont = (230, 230, 230, 128)
blackFont = (0, 0, 0)

import requests

url = "https://x125.ru/api/school/randomword"

headers = {
    "Content-Type": "application/json",
    "Authorization": "Token 11609376-ff57-401e-88a4-53f4c0904fdb"
}

response = requests.request("POST", url, headers=headers).json()

draw.text((W/2, H/2 - 130), response['word'], font=boldfont52, fill=blackFont, anchor="mm")
draw.text((W/2, H/2), response['articulation'], font=font44, fill=blackFont, anchor="mm")
draw.text((W/2, H/2 + 70), response['translation'], font=font32, fill=blackFont, anchor="mm")

print(response)

# draw.line((CENTER, LINESTART, CENTER, H), fill=greyFont, width=1)
# This method will show image in any image viewer
im.show()
