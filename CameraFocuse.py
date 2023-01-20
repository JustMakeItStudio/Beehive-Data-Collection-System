from cv2 import VideoCapture, imshow, waitKey

cam = VideoCapture(0)
if not cam.isOpened():
    raise Exception('Debug: Camera did not initialise.')
cam.set(3, 1280)
cam.set(4, 720)

print("Focus frame, use the white circular key to adjust the focus of the camera")

while 1:
    ret, frame = cam.read()
    imshow("Focus frame, use the white circular key to adjust the focus of the camera", frame)
    waitKey(1)