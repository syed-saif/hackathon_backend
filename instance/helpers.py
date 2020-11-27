import io
import os
import re
from google.cloud import vision
from django.conf import settings

def detect_document(path):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = settings.GOOGLE_APPLICATION_CREDENTIALS
    client = vision.ImageAnnotatorClient()
    with io.open(path, 'rb') as image_file:
        content = image_file.read()
    image = vision.Image(content=content)
    response = client.document_text_detection(image=image)
    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))
    return response.full_text_annotation.text


def getPart(s, part=1):
    out = s.split('=')[part].strip()
    return out

def detect_handwritten_image(detect_handwritten):
    detect_text = detect_document(detect_handwritten.image.path)
    print(detect_text)
    try:
        part1_text = getPart(detect_text, 0)
        part2_text = getPart(detect_text, 1)
        final_val = True if eval(part1_text) == eval(part2_text) else False
        return True, final_val
    except:
        pass
    return False, False