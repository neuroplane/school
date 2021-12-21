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
H = 384
W = 640

im = PIL.Image.new(mode="RGB", size=(640, 384), color=(255, 255, 255))
draw = ImageDraw.Draw(im)
###############################################
boldfont52 = ImageFont.truetype('fonts/charisbold.ttf', 52)
font52 = ImageFont.truetype('fonts/charis.ttf', 52)
font44 = ImageFont.truetype('fonts/charis.ttf', 44)
font32 = ImageFont.truetype('fonts/charis.ttf', 32)
font24 = ImageFont.truetype('fonts/charis.ttf', 24)
font16 = ImageFont.truetype('fonts/charis.ttf', 16)
greyFont = (230, 230, 230, 128)
blackFont = (0, 0, 0)

url = "https://x125.ru/api/school/randomword"

headers = {
    "Content-Type": "application/json",
    "Authorization": "Token 11609376-ff57-401e-88a4-53f4c0904fdb"
}

response = requests.request("POST", url, headers=headers).json()

draw.text((W / 2, H / 2 - 120), response['word'], font=boldfont52, fill=blackFont, anchor="mm")
draw.text((W / 2, H / 2 - 50), response['articulation'], font=font44, fill=blackFont, anchor="mm")
draw.text((W / 2, H / 2 ), response['translation'], font=font24, fill=blackFont, anchor="mm")
if response['example_en'] is not None:
    draw.text((W / 2, H / 2 + 60), response['example_en'], font=font16, fill=blackFont, anchor="mm")
if response['example_ru'] is not None:
    draw.text((W / 2, H / 2 + 90), response['example_ru'], font=font16, fill=blackFont, anchor="mm")

print(response)

im.show()
