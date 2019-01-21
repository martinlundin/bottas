# -*- coding: utf-8 -*-
import cv2
import pytesseract
from PIL import Image
import bing
import pointify
import afilter
import pyautogui
import urllib.request
import numpy as np
import re

class Text(object):
    def __init__(self, id, position, color=(0, 0, 0)):
        self.id = id
        self.position = position
        self.color = color
        self.content = {
            "sv": "",
            "en": ""
        }
        self.pointify = {
            "points": 0,
            "hits": 0,
        }

    id = 0
    position = {
        'x': [0, 0],
        'y': [0, 0]
    }
    content = {
        "sv": "",
        "en": ""
    }
    color = (0, 0, 0)
    image = ""
    pointify = {
        "points": 0,
        "hits": 0,
    }


# Objects
# q = question
# alt = alternatives, a = alternative
q = Text(100, {'x': [25, 660], 'y': [195, 370]})
alt = []
alt.append(Text(1, {'x': [30, 640], 'y': [440, 505]}, color=(68, 165, 255)))
alt.append(Text(2, {'x': [30, 640], 'y': [550, 615]}, color=(68, 213, 255)))
alt.append(Text(3, {'x': [30, 640], 'y': [660, 725]}, color=(68, 255, 204)))

# Settings
dev = False
cutoff = 150
guest = None

# Functions
def screenshot_to_text():
    #Take screenshot

    pyautogui.screenshot('img/screenshot.png')
    image = cv2.imread('img/screenshot.png')
    image = image[190:1400, 30:700]

    # Crop image
    q.image = image[q.position['y'][0]:q.position['y'][1], q.position['x'][0]:q.position['x'][1]]
    for a in alt:
        a.image = image[a.position['y'][0]:a.position['y'][1], a.position['x'][0]:a.position['x'][1]]

    # Read question image to text
    q.content['sv'] = bing.ocr(q.image)
    if dev: cv2.imwrite('img/q/' + str(q.id) + '.png', q.image)
    q.content['sv'] = q.content['sv'].replace("?", "")
    print(q.content['sv'])
    # Read alternatives image to text
    for a in alt:
        a.content['sv'] = bing.ocr(a.image)
        if dev: cv2.imwrite('img/a/' + str(a.id) + '.png', a.image)
        print(a.content['sv'])

        # If content is empty we need to do another ocr
        if a.content['sv'] == "" or a.content['sv'] == " ":
            a.image = cv2.cvtColor(a.image, cv2.COLOR_BGR2GRAY)
            a.image = cv2.inRange(a.image, cutoff, 255)
            if dev: cv2.imwrite('img/a/' + str(a.id) + '_to_tes.png', a.image)
            a.content['sv'] = pytesseract.image_to_string(Image.fromarray(a.image), lang="swe")
            print(a.content['sv'])
            if a.content['sv'] == "" or a.content['sv'] == " ":
                a.content['sv'] = pytesseract.image_to_string(Image.fromarray(a.image), lang="swe", config='-psm 10')
                print(a.content['sv'])

# Create window
cv2.namedWindow("omg", cv2.WINDOW_NORMAL)
cv2.moveWindow("omg", 370, 0)
cv2.resizeWindow('omg', 340, 650)
imageHolder = cv2.imread('img/holder.jpg')
cv2.imshow("omg", imageHolder)

while True:
    k = cv2.waitKey(1)

    if k % 256 == 115:
        cutoff = cutoff + 5
        print(cutoff)
    if k % 256 == 97:
        cutoff = cutoff - 5
        print(cutoff)

    if k % 256 == 27:
        # ESC pressed
        print("[ESC]", '\n')
        break

    if k % 256 == 105:
        # I pressed
        print("[I]", '\n')

        screenshot_to_text()

        # Search images
        i = 0
        for a in alt:
            # Pure alternative
            bingResults = bing.search(a.content['sv'], type="images")

            if bingResults['value']:
                imageResult = bingResults['value'][0]['thumbnailUrl']
                imageResult = urllib.request.urlopen(imageResult)
                imageResult = np.asarray(bytearray(imageResult.read()), dtype="uint8")
                imageResult = cv2.imdecode(imageResult, cv2.IMREAD_COLOR)
                cv2.namedWindow(a.content['sv'], cv2.WINDOW_NORMAL)
                cv2.imshow(a.content['sv'], imageResult)
                cv2.moveWindow(a.content['sv'], 700, i)

            #Question + alternative
            bingResults = bing.search(q.content['sv'] + " " + a.content['sv'], type="images")
            if bingResults['value']:
                imageResult = bingResults['value'][0]['thumbnailUrl']
                imageResult = urllib.request.urlopen(imageResult)
                imageResult = np.asarray(bytearray(imageResult.read()), dtype="uint8")
                imageResult = cv2.imdecode(imageResult, cv2.IMREAD_COLOR)
                cv2.namedWindow(q.content['sv'] + " " + a.content['sv'], cv2.WINDOW_NORMAL)
                cv2.imshow(q.content['sv'] + " " + a.content['sv'], imageResult)
                cv2.moveWindow(q.content['sv'] + " " + a.content['sv'], 1100, i)

            i += 300

    if k % 256 == 114:
        # R pressed
        print("[R]", '\n')
        guest = input('Guest: ')

    if k % 256 == 32:
        # SPACE pressed
        print("[SPACE]", '\n')
        print(guest)

        screenshot_to_text()

        # If "jag" in question
        if "jag" in q.content['sv'] and guest != None:
            q.content['sv'].replace("jag", guest)

        # Bundle searches into array
        searches = []
        searches.append(q.content['sv'])
        searches.append(afilter.rm_fwords(q.content['sv']))

        # Question includes quotes, search for that content
        quotes = re.findall('"([^"]*)"', q.content['sv'])
        if quotes:
            searches.append(quotes[0])

        # Captial letter words are usually important, add it to the search
        #first = True
        #capital_words = []
        #for word in q.content['sv'].split():
        #    if word[0].istitle() and first is False:
        #        capital_words.append(word)
        #    first = False
        #if capital_words:
        #    searches.append(' '.join(capital_words))

        # Perform searches
        bingResults = bing.search(searches)

        # Get points
        alt = pointify.bing(bingResults, alt)

        print("\n")
        text = ""
        for a in alt:
            print(a.content['sv'], a.pointify['points'], '('+str(a.pointify['hits'])+')')
            text += "[" + str(a.pointify['points']) + ' ('+str(a.pointify['hits'])+')]   '

        # If bingPoints are empty do "reverse search"
        if all(a.pointify['hits'] == 0 for a in alt):
            print('REVERSE SEARCH RESULTS...', '\n')
            for a in alt:
                print('----------------------------')
                bingResults = bing.search(a.content['sv'])
                bingPoints = pointify.bingReverse(bingResults, afilter.rm_fwords(q.content['sv']).split())
                print(a.content['sv'], '\n')
                for point in bingPoints:
                    if bingPoints[point] != 0:
                        print(point, bingPoints[point])

cv2.destroyAllWindows()