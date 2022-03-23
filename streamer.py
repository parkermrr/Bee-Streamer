from flask import Response
from flask import Flask
from flask import render_template
import threading
import argparse
import datetime
import time
import cv2
from waitress import serve

# initialize the output frame and a lock used to ensure thread-safe exchanges of the output frames
outputFrame = None
lock = threading.Lock()

# initialize a flask object
app = Flask(__name__)

# initialize the video stream and allow the camera sensor to warm up
vs = cv2.VideoCapture(0)
vs.set(3,1920)
vs.set(4,1080)
vs.set(cv2.CAP_PROP_FPS, 60.0)
time.sleep(2.0)

@app.route("/")
def index():
	# return the rendered template
	return render_template("index.html")

def camera_preprocess():
	global vs, outputFrame, lock

	while True:
		# read the next frame from the video stream
		ret, frame = vs.read()

		with lock:
			outputFrame = frame.copy()

def generate():
	# grab global references to the output frame and lock variables
	global outputFrame, lock
	# loop over frames from the output stream
	while True:
		# wait until the lock is acquired
		with lock:
			# check if the output frame is available, otherwise skip
			# the iteration of the loop
			if outputFrame is None:
				continue
			# encode the frame in JPEG format
			(flag, encodedImage) = cv2.imencode(".jpg", outputFrame)
			# ensure the frame was successfully encoded
			if not flag:
				continue
		# yield the output frame in the byte format
		yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 
			bytearray(encodedImage) + b'\r\n')

@app.route("/video_feed")
def video_feed():
	# return the response generated along with the specific media
	# type (mime type)
	return Response(generate(),
		mimetype = "multipart/x-mixed-replace; boundary=frame")

# check to see if this is the main thread of execution
if __name__ == '__main__':
	# construct the argument parser and parse command line arguments
	# start a thread that will read from the camera
	t = threading.Thread(target=camera_preprocess)
	t.daemon = True
	t.start()
	# start the flask app
	# app.run(host='0.0.0.0', port=8000, debug=True,
	# 	threaded=True, use_reloader=False)
	serve(app, host='0.0.0.0', port=8000)