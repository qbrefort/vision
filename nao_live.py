import sys
from naoqi import ALProxy
import time
import almath
import sys
import cv2
import Image

global tts
global camProxy
global var
global motionProxy
global post
global IP
global PORT

def naom(name, angle):
	global motionProxy
	motionProxy.setAngles(name,angle*almath.TO_RAD,0.7)

def itsyou():
	global tts
	global motionProxy
	naom("RShoulderRoll", 0.0)
	naom("RShoulderPitch", 0.0)
	naom("RElbowRoll", 0.0)
	naom("RElbowYaw", 0.0)
	naom("RWristYaw", 90.0)
	motionProxy.openHand("RHand")
	tts.say("I find your lack of faith disturbing.")
	time.sleep(1.0)
	motionProxy.closeHand("RHand")
	time.sleep(4.0)
	naom("RShoulderPitch", 75.0)

def liveSpeak():
	global tts
	tts.say("Hello!")
	w = True
	while w:
		sentence = raw_input();
		if sentence == "quit":
			w = False
			tts.say("Goodbye")
		else:
			tts.say(sentence)

def showNaoImage():
	global camProxy
	resolution = 1    # VGA
	colorSpace = 11   # RGB
	videoClient = camProxy.subscribe("python_client", resolution, colorSpace, 5)
	# Get a camera image.
	# image[6] contains the image data passed as an array of ASCII chars.
	naoImage = camProxy.getImageRemote(videoClient)
	camProxy.unsubscribe(videoClient)
	# Get the image size and pixel array.
	imageWidth = naoImage[0]
	imageHeight = naoImage[1]
	array = naoImage[6]
	# Create a PIL Image from our pixel array.
	im = Image.fromstring("RGB", (imageWidth, imageHeight), array)
	# Show the image.
	im.save("camImage.png", "PNG")

class Tracker:
	global motionProxy		

	def __init__(self):
		cv2.namedWindow("TrackerWindow", cv2.CV_WINDOW_AUTOSIZE)
		self.scale = 1
		self.scale_down = 1

	def run(self):  
		while True:
			#f, orig_img = self.capture.read()
			#orig_img = cv2.imread("naoimg_004.png");
			showNaoImage()
			orig_img = cv2.imread("camImage.png");
			cv2.imshow("TrackerWindow", orig_img)
	
			key = cv2.waitKey(20)
			print key
			if key == 1048603:
				cv2.destroyWindow("TrackerWindow")
				break
			elif key == 122:
				motionProxy.moveTo(0.1, 0.0, 0.0)
			elif key == 115:
				motionProxy.moveTo(-0.1, 0.0, 0.0)
			elif key == 100:
				motionProxy.moveTo(0.0, 0.1, 0.0)
			elif key == 113:
				motionProxy.moveTo(0.0, -0.1, 0.0)
			elif key == 97:
				motionProxy.moveTo(0.0, 0.0, 10*almath.TO_RAD)
			elif key == 101:
				motionProxy.moveTo(0.0, 0.0, -10*almath.TO_RAD)			
			else:
				key = 0
	
		
if __name__ == "__main__":
	IP = "172.20.12.26"
	PORT = 9559
	tts = ALProxy("ALTextToSpeech", IP, PORT)
	camProxy = ALProxy("ALVideoDevice", IP, PORT)
	motionProxy = ALProxy("ALMotion", IP, PORT)
	post = ALProxy("ALRobotPosture", IP, PORT)
	tts.setLanguage("English")
	tts.setVolume(1.0)
	
	post.goToPosture("Stand", 1.0)
	time.sleep(1.0)
	tts.say("S C V Ready !")
	tracker = Tracker()

	while True:
		command = raw_input()
		if command=='sp':
			liveSpeak()
		if command=='im':
			showNaoImage()
		if command=='oh':
			itsyou()
		if command=='dep':
			tracker.run()
		if command=='init':
			post.goToPosture("Crouch", 1.0)
		if command=='exit':
			break

	post.goToPosture("Sit", 1.0)
	time.sleep(1.0)
	tts.say("Standing by")
	motionProxy.setStiffnesses("Body", 0.0)