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

#run through this for every image.
#replace the below function in the code.
def detect_handwritten_image(detect_handwritten):
    detect_text = detect_document(detect_handwritten.image.path)
    result=[]
    sep_expressions = detect_text.split('\n')
    for i in sep_expressions:
        try:
            isExp = i.find('=')
            if (isExp == -1): 
                continue
            part1_text = getPart(i, 0).replace('x','*')
            part2_text = getPart(i, 1).replace('x','*')
            final_val = True if eval(part1_text) == eval(part2_text) else False
            result.append({'exp' : i,'isValid' : final_val})
        except Exception as e:
            pass
    if(len(result) == len(sep_expressions)):
        status = 'completed'
    elif (len(result) == 0):
        status = 'failed'
    else:
        status = 'partial'
    print(result, status)
    return result, status