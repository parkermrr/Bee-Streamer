gst-launch-1.0 -v v4l2src device="/dev/video0" ! "video/x-raw,width=1920,framerate=30/1" ! videoconvert ! x264enc bitrate=1024 ! video/x-h264,profile=\"high\" ! \
mpegtsmux ! hlssink playlist-root=http://10.37.97.64:8000 location=segment_%05d.ts target-duration=5 max-files=5
