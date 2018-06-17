from PIL import Image, ImageStat
import time,math
import cv2
import requests
import json
import serial
from random import randint
from IPython.display import HTML
import sys

ser = serial.Serial ('/dev/ttyUSB0',9600, timeout=.5)
def color(R, G, B):
    finalString = '(T'+ str(R) +',' + str(G) + ',' + str(B) + ',)'
    print finalString
    ser.write(finalString)
    #while ser.read != "done":

def adjust_brigtness(brightness):
    normalizedBr = 100*brightness/255
    
    
def calculate_brightness(im_file):
   im = Image.open(im_file)
   stat = ImageStat.Stat(im)
   r,g,b = stat.mean
   return math.sqrt(0.241*(r**2) + 0.691*(g**2) + 0.068*(b**2))  
while True:
	camera_port = 0
	camera = cv2.VideoCapture(camera_port)
	time.sleep(0.1)  # If you don't wait, the image will be dark
	return_value, image = camera.read()
	cv2.imwrite("opencv.jpg", image)
	del(camera)  # so that others can use the camera as soon as possible
        print "Camere done"
	#Evaluate a picture
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
        brightness = calculate_brightness(image_path)
 	headers = {'Content-Type': 'application/octet-stream','Ocp-Apim-Subscription-Key': subscription_key}

	params = {
	    'returnFaceId': 'true',
	    'returnFaceLandmarks': 'false',
	    'returnFaceAttributes': 'emotion'
	}

	response = requests.post(face_api_url, params=params, headers=headers,data=image_data)
	faces = response.json()

	jsonToPython = json.dumps(faces, indent=4)
	datastore = json.loads(jsonToPython)

	happyValue = datastore[0]["faceAttributes"]["emotion"]["happiness"]
        sadValue = datastore[0]["faceAttributes"]["emotion"]["sadness"]

        print happyValue, sadValue
        if (happyValue > 0.5):
           #isHappy = True
           randNum = randint(0, 2)
           if (randNum==0):
              color(0,0,255)
           elif (randNum ==1):
               color(255,140,0)
           else:
               color(255,0,0)   
        elif(happyValue <0.5 and sadValue > 0.5):
           #isHappy = False
           randNum = randint(0, 2)
           if (randNum==0):
              color(255,255,0)
           elif (randNum ==1):
              color(95,61,176)
           else:
               color(144,238,144) 
        else:
           color(randint(0, 255), randint(0, 255), randint(0, 255))
        #add DONE @ serial
        #adjust_brightness(brightness) 
        time.sleep(10)

