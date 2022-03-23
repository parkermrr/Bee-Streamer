# import the opencv library
import cv2

# define a video capture object
vid = cv2.VideoCapture(0)
codec = 0x47504A4D  # MJPG
vid.set(cv2.CAP_PROP_FOURCC, codec)
vid.set(3,1920)
vid.set(4,1080)
vid.set(cv2.CAP_PROP_FPS, 24.0)

fps = vid.get(cv2.CAP_PROP_FPS)
print("Frames per second: {0}".format(fps))

codec = vid.get(cv2.CAP_PROP_FOURCC)
print(codec)

while(True):
      
    # Capture the video frame
    # by frame
    ret, frame = vid.read()
  
    # Display the resulting frame
    cv2.imshow('frame', frame)
      
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
  
# After the loop release the cap object
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()