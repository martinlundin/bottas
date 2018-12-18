# -*- coding: utf-8 -*-
import requests, time, http.client, uuid, json, cv2

dev = False

# noinspection PyPackageRequirements
def search(texts, lang="sv-SE", type="web"):
    # If texts is not an array, it should be transformed into one
    if not isinstance(texts, list):
        texts = [texts]

    subscription_key = "9fae0505eec8485c90ddc2dc6ae9976a"
    if dev: subscription_key = "9fae0505eec8485c90ddc2dc6ae9976a"

    assert subscription_key

    if type == "images":
        search_url = "https://api.cognitive.microsoft.com/bing/v7.0/images/search"
    else:
        search_url = "https://api.cognitive.microsoft.com/bing/v7.0/search"

    headers = {"Ocp-Apim-Subscription-Key": subscription_key}

    results = []

    count = 30
    if type == "images": count = 1

    for text in texts:
        params = {"q": text, "textDecorations": True, "count": count, "textFormat": "HTML", "mkt": lang}
        # noinspection PyPackageRequirements
        response = requests.get(search_url, headers=headers, params=params)
        response.raise_for_status()
        results.append(response.json())
        if dev: time.sleep(0.33)

    if len(results) == 1:
        results = results[0]

    return results


def ocr(image):
    subscription_key = "bd9df09c4d09412f9ec22d8505baebf5"
    assert subscription_key
    vision_base_url = "https://northeurope.api.cognitive.microsoft.com/vision/v2.0/"

    analyze_url = vision_base_url + "ocr"

    # Read the image into a byte array
    image_data = cv2.imencode('.png', image)[1].tostring()

    headers = {'Ocp-Apim-Subscription-Key': subscription_key,
               'Content-Type': 'application/octet-stream'}
    params = {'language': 'sv', 'detectOrientation': 'false'}
    response = requests.post(
        analyze_url, headers=headers, params=params, data=image_data)
    response.raise_for_status()

    # The 'analysis' object contains various fields that describe the image. The most
    # relevant caption for the image is obtained from the 'description' property.
    analysis = response.json()

    line_infos = [region["lines"] for region in analysis["regions"]]
    words = []
    for line in line_infos:
        for word_metadata in line:
            for word_info in word_metadata["words"]:
                words.append(word_info["text"])
    sentence = " ".join(words)
    return sentence

def translate(texts, to_lang="en", from_lang="sv"):
    subscriptionKey = '33c6105d42434d428b77566f3aab9500'
    host = 'api.cognitive.microsofttranslator.com'
    path = '/translate?api-version=3.0'

    # If texts is not an array, it should be transformed into one
    if not isinstance(texts, list):
        texts = [texts]

    params = "&to=" + to_lang + "&from=" + from_lang

    headers = {
        'Ocp-Apim-Subscription-Key': subscriptionKey,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    requestBody = []
    for text in texts:
        requestBody.append({'Text': text})

    content = json.dumps(requestBody, ensure_ascii=False).encode('utf-8')

    conn = http.client.HTTPSConnection(host)
    conn.request("POST", path + params, content, headers)
    response = conn.getresponse()
    json_responses = json.loads(response.read())

    returnArray = []
    for json_response in json_responses:
        returnArray.append(json_response['translations'][0]['text'])

    if len(returnArray) == 1:
        returnArray = returnArray[0]

    return returnArray
