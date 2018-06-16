# Replace <Subscription Key> with your valid subscription key.

import requests

subscription_key = "82d9b1e05e16413d8bcca30f32b1ca83"
assert subscription_key

# You must use the same region in your REST call as you used to get your
# subscription keys. For example, if you got your subscription keys from
# westus, replace "westcentralus" in the URI below with "westus".
#
# Free trial subscription keys are generated in the westcentralus region.
# If you use a free trial subscription key, you shouldn't need to change
# this region.
face_api_url = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0/detect'
#face_api_url = 'https://westcentralus.api.cognitive.microsoft.com/emotion/v1.0/recognize'
# Set image_url to the URL of an image that you want to analyze.
#image_url = '/home/ess/Documents/TechFest/happy.jpg'
image_url = 'http://farm3.static.flickr.com/2226/2140577195_61d14b7dc3.jpg'

image_path = "/home/ess/Documents/TechFest/happy.jpg"
image_data = open(image_path, "rb").read()
headers = {'Ocp-Apim-Subscription-Key': subscription_key}

response = requests.post(face_api_url, headers=headers, data=image_data)
response.raise_for_status()
analysis = response.json()
analysis


headers = {'Ocp-Apim-Subscription-Key': subscription_key}



response = requests.post(
    face_api_url, params=params, headers=headers, json={"url": image_url})
faces = response.json()

# Display the original image and overlay it with the face information.
# If you are using a Jupyter notebook, uncomment the following line.
#%matplotlib inline
"""
import matplotlib.pyplot as plt
from PIL import Image
from matplotlib import patches
from io import BytesIO

#response = requests.get(image_url)
#image = Image.open(BytesIO(response.content))
plt.figure(figsize=(5,5))
image= Image.open('/home/ess/Documents/TechFest/happy.jpg')
#image  = Image.open(BytesIO(image_data))
ax     = plt.imshow(image, alpha=0.6)

for face in analysis:
    fr = face["faceRectangle"]
    em = face["scores"]
    origin = (fr["left"], fr["top"])
    p = Rectangle(origin, fr["width"], fr["height"], fill=False, linewidth=2, color='b')
    ax.axes.add_patch(p)
    ct = "\n".join(["{0:<10s}{1:>.4f}".format(k,v) for k, v in sorted(list(em.items()),key=lambda r: r[1], reverse=True)][:3])
    plt.text(origin[0], origin[1], ct, fontsize=20)    
_ = plt.axis("off")"""

"""plt.figure(figsize=(8, 8))
ax = plt.imshow(image, alpha=0.6)
for face in faces:
    fr = face["faceRectangle"]
    fa = face["faceAttributes"]
    origin = (fr["left"], fr["top"])
    p = patches.Rectangle(
        origin, fr["width"], fr["height"], fill=False, linewidth=2, color='b')
    ax.axes.add_patch(p)
    plt.text(origin[0], origin[1], "%s, %d"%(fa["gender"].capitalize(), fa["age"]),
             fontsize=20, weight="bold", va="bottom")
_ = plt.axis("off")"""
