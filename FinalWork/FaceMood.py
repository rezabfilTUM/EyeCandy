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

# Set image_url to the URL of an image that you want to analyze.
image_url = 'http://farm3.static.flickr.com/2226/2140577195_61d14b7dc3.jpg'

image_path = "/home/ess/Documents/TechFest/EyeCandy/FinalWork/opencv.jpg"
image_data = open(image_path, "rb").read()

import requests
import json

from IPython.display import HTML

headers = {'Content-Type': 'application/octet-stream','Ocp-Apim-Subscription-Key': subscription_key}

params = {
    'returnFaceId': 'true',
    'returnFaceLandmarks': 'false',
    'returnFaceAttributes': 'emotion'
}
#json={"url": image_url}
response = requests.post(face_api_url, params=params, headers=headers,data=image_data)
faces = response.json()

jsonToPython = json.dumps(faces, indent=4)
datastore = json.loads(jsonToPython)
print datastore
print "\n new"
print datastore[0]["faceAttributes"]["emotion"]["happiness"]

happyValue = datastore[0]["faceAttributes"]["emotion"]["happiness"]
#print json.dumps('faceAttributes')
"""
# Display the original image and overlay it with the face information.
# If you are using a Jupyter notebook, uncomment the following line.
#%matplotlib inline
import matplotlib.pyplot as plt
from PIL import Image
from matplotlib import patches
from io import BytesIO

response = requests.get(image_url)
image = Image.open(BytesIO(response.content))

plt.figure(figsize=(8, 8))
ax = plt.imshow(image, alpha=0.6)
for face in faces:
    fr = face["faceRectangle"]
    #em = face["scores"]
    fa = face["faceAttributes"]
    print "\nNEW ATTT", fa
    for facing in fa:
        emotin = facing[0][0]
        emotin2 = facing[1]
        emotin3 = facing[2]
        emotin4 = facing[3]
        print emotin, emotin2, emotin3, emotin4
        
    #
    origin = (fr["left"], fr["top"])
    p = patches.Rectangle(
        origin, fr["width"], fr["height"], fill=False, linewidth=2, color='b')
    ax.axes.add_patch(p)
    #ct = "\n".join(["{0:<10s}{1:>.4f}".format(k,v) for k, v in sorted(list(em.items()),key=lambda r: r[1], reverse=True)][:3])
    #plt.text(origin[0], origin[1], ct, fontsize=20)  
    plt.text(origin[0], origin[1], "%s, %d"%(fa["gender"].capitalize(), fa["age"]),
             fontsize=20, weight="bold", va="bottom")
_ = plt.axis("off")"""
