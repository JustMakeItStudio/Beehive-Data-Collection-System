from cv2 import VideoCapture, destroyAllWindows, imwrite
import time
import os


class Camera:

    def __init__(self, fileDirImages, framerate, width, height, startTimeVideo, endTimeVideo, debug):
        self.debug = debug
        self.framerate = framerate
        self.cam = VideoCapture(0)
        if not self.cam.isOpened():
            self.printDebug('Camera did not initialise.', self.debug)
            raise Exception('Camera did not initialise, restart.')
        self.cam.set(3, width)
        self.cam.set(4, height)
        self.imageName = fileDirImages # still needs to add the name, now it has only the directory to be saved
        self.startTimeVideo = startTimeVideo # what time will the camera start recording
        self.endTimeVideo = endTimeVideo # what time will the camera stop recording
        
    def captureImages(self):
        timeBetweenEachFrame = 1 / self.framerate # converting framerate into waiting time in seconds between frames
        timePassed = 0
        elapsedTime = 0
        i = 0 # The frame number within one second, it resets after each second
        try:
            while True:
                theTimeNowAsString = time.strftime("%Y_%m_%d-%H%M%S")            
                #  Test if it's night
                if self.isNight(theTimeNowAsString):
                    continue

                startTime = time.time()
                
                if timePassed >= timeBetweenEachFrame:
                    ret, frame = self.cam.read()
                    if ret:
                        dateForFileName = time.strftime("%Y_%m_%d")
                        try:
                            os.mkdir(f'{self.imageName}/{dateForFileName}/')
                        except:
                            pass
                        fileName = f'{self.imageName}/{dateForFileName}/{theTimeNowAsString} {i}.jpg'                  
                        imwrite(fileName, frame)
                    timePassed = 0
                    if i < self.framerate:
                        # This might be a bug
                        i += 1
                    else:
                        i = 0
                
                elapsedTime = time.time() - startTime
                timePassed = timePassed + elapsedTime
                elapsedTime = 0

        except Exception as e:
            self.printDebug(e, self.debug)
            self.closeAllCameras()
    
    def isNight(self, theTimeNow: str):
        # if it's night then dont take pictures
        hour = theTimeNow[-6:-4] # as string
        if hour[0] == '0':
            hour = int(hour[1])
        else:
            hour = int(hour)
        
        if hour < self.startTimeVideo or hour > self.endTimeVideo:
            return True
        else:
            return False

    def printDebug(self, msg: str, debug: bool):
        if debug:
            print(f'Debug: {msg}')
            with open('debug.txt', 'a') as f:
                f.write(f'{time.strftime("%Y_%m_%d-%H%M%S")} {msg}')
                f.write('\n')

    def closeAllCameras(self):
        self.cam.release()
        destroyAllWindows()
