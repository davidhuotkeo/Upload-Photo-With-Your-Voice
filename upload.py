# import libraries
import requests
import json
from io import BytesIO
from PIL import Image
import numpy as np
import os
from InstagramAPI import InstagramAPI
import speech_recognition as sr

#############################################################################
#   To use the it, must close 2 form factor security in your insta profile  #
#############################################################################

# request cat api
main_request = requests.get('https://api.thecatapi.com/v1/images/search')
content = main_request.content.decode()

# serialize json object and load it
jsonified = json.loads(content)

# get the image url with json from cat api
# that output looks like this
# [
#     {
#         "breeds": [],
#         "id": "MTYzOTc2NQ",
#         "url": "https://cdn2.thecatapi.com/images/MTYzOTc2NQ.jpg",
#         "width": 500,
#         "height": 750
#     }
# ]
url_image = jsonified[0]['url']

# request the image url
request_image = requests.get(url_image)
image_content = request_image.content

# create image using pillow lib
image_bytes = BytesIO(image_content)
image = Image.open(image_bytes)

# if the cat folder is not exist make and count the number files in it
cat_folder = os.path.exists('cat')
if not cat_folder:
    os.makedirs('cat')
dir = os.listdir('cat')
num_pic = len(dir)

# save the image
picture_name = "cat/{}.jpg".format(num_pic)
image.save(picture_name)

# login to your account
insta = InstagramAPI('', '')
insta.login()

# voice recognition
# I name my recognition tesla
recognition = sr.Recognizer()

with sr.Microphone() as source:
    print('Say something')
    voice = recognition.listen(source)

voice_output = recognition.recognize_google(voice).lower()

print(voice_output)

# output the voice and action
if 'tesla' in voice_output:
    if 'post' in voice_output:
        caption = "Posted with love by Python Code using Cat API"
        insta.uploadPhoto(picture_name, caption=caption)
