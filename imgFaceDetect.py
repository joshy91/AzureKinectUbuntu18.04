import asyncio
import io
import glob
import os
import sys
import time
import uuid
import requests
from urllib.parse import urlparse
from io import BytesIO
from PIL import Image, ImageDraw
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.face.models import TrainingStatusType, Person, SnapshotObjectType, OperationStatusType
# Set the FACE_SUBSCRIPTION_KEY environment variable with your key as the value.
# This key will serve all examples in this document.
KEY = '327f69fc7c46434283cf8aace49cb300'

# Set the FACE_ENDPOINT environment variable with the endpoint from your Face service in Azure.
# This endpoint will be used in all examples in this quickstart.
ENDPOINT = 'https://azurefacetest.cognitiveservices.azure.com/'
# Create an authenticated FaceClient.
face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))
# Detect a face in an image that contains a single face
single_face_image_url = 'https://scontent.fftw1-1.fna.fbcdn.net/v/t1.0-9/75246719_3143930229014650_4410890718176870400_o.jpg?_nc_cat=111&_nc_ohc=S80GrPqEjHoAQkUrvo8Ud12aH3sTeLfCdttN_TzJV9CVQZoCV3q7CzTzA&_nc_ht=scontent.fftw1-1.fna&oh=f87f4a936cbe14a8ea977c1b0307dab9&oe=5E892BF9'
single_image_name = os.path.basename(single_face_image_url)
detected_faces = face_client.face.detect_with_url(url=single_face_image_url)
if not detected_faces:
    raise Exception('No face detected from image {}'.format(single_image_name))

# Convert width height to a point in a rectangle
def getRectangle(faceDictionary):
    rect = faceDictionary.face_rectangle
    left = rect.left
    top = rect.top
    bottom = left + rect.height
    right = top + rect.width
    return ((left, top), (bottom, right))


# Download the image from the url
response = requests.get(single_face_image_url)
img = Image.open(BytesIO(response.content))

# For each face returned use the face rectangle and draw a red box.
print('Drawing rectangle around face... see popup for results.')
draw = ImageDraw.Draw(img)
for face in detected_faces:
    draw.rectangle(getRectangle(face), outline='red')

# Display the image in the users default image browser.
img.show()

import requests
import json

# set to your own subscription key value
subscription_key = '327f69fc7c46434283cf8aace49cb300'
assert subscription_key

# replace <My Endpoint String> with the string from your endpoint URL
face_api_url = 'https://azurefacetest.cognitiveservices.azure.com/face/v1.0/detect'

headers = {'Ocp-Apim-Subscription-Key': KEY}

params = {
    'returnFaceId': 'true',
    'returnFaceLandmarks': 'false',
    'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise',
}

response = requests.post(face_api_url, params=params,
                         headers=headers, json={"url": single_face_image_url})
print(json.dumps(response.json()))

