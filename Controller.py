# Controller class, handling everything 

# To send messages on whats-app use https://www.callmebot.com/blog/telegram-text-messages/

try:
    import time
    from multiprocessing import Process
    import os

    ''' Import our .py files '''
    from Sensor import Sensors
    from AudioHandling import Audio
    from PictureHandling import Camera
    
    ''' User Editable Variables '''
    hiveID = 'TEST'
    debug = True
    storageWarningThreshold = 90 # Percentage
    phoneNumbers = [99999999, 99999999] # Replace with correct one.
    phoneNumbersKeys = [99999, 99999] # Replace with correct one.
    wifiName = 'wifiname' 
    wifiPassword = 'password' 
    timeDurationAudio = 1 # seconds, collecting sound and saving it. The optimal time is calulated by trial and error
    timeIntervalTemperatureAndHumidity = 60*15 # seconds, every 15 minutes
    timeIntervalWeight = 60*60*2 # seconds, every 2 hours
    framerate = 6 # frames/sec
    imageWidth = 1280 # pixels
    imageHeight = 720 # pixels
    startTimeVideo = 7 # start recording images at 5 in the morning every day
    endTimeVideo = 17 # stop recording images at 20 in the night every day
    sampRate = 44100 # audio sample rate hz
    nameOfMicrophoneDevice = 'Sound Blaster Play! 3'
    roundingAmountOfEachSample = 5

    def printDebug(msg: str, debug: bool):
        if debug:
            print(f'Debug: {msg}')
            with open('debug.txt', 'a') as f:
                f.write(f'{time.strftime("%Y_%m_%d-%H%M%S")} {msg}')
                f.write('\n')
            
    
    ''' Try to connect to a specific WiFi '''   
    try:
        # This is not working yet
        os.system('sudo iwconfig wlan0 essid ' + wifiName + ' key ' + wifiPassword)
        printDebug('Successfully connected to the WiFi', debug)
    except:
        printDebug('Didnt connect to the wifi', debug)

    
    ''' Create the file directory that data will be saved into '''    
    try:
        # If there is an external ssd then create there the file directories
        printDebug(f'found something {os.listdir("/media/pi")[0]}', debug)
        nameOfUSBStorage = os.listdir("/media/pi")[0]
        dataName = f'BeeHive-{hiveID}_'
        try:
            os.mkdir(f'/media/pi/{nameOfUSBStorage}/{dataName}Data/')
        except FileExistsError:
            printDebug("Directory Data on the SSD either already exists or it was not created.", debug)
            
        try:
            os.mkdir(f'/media/pi/{nameOfUSBStorage}/{dataName}Data/Images/')
        except FileExistsError:
            printDebug("Directory Data/Images on the SSD either already exists or it was not created.", debug)
        try:
            os.mkdir(f'/media/pi/{nameOfUSBStorage}/{dataName}Data/Audio/')
        except FileExistsError:
            printDebug("Directory Data/Audio on the SSD either already exists or it was not created.", debug)
            
        saveDir = f'/media/pi/{nameOfUSBStorage}'
    except Exception as e:
        printDebug('There is a usb connected but it is not a storage device.', debug)
        printDebug(e, debug)
        try:
            os.mkdir(f'/home/pi/Desktop/{dataName}Data/')
        except FileExistsError:
            printDebug("Directory Data on desktop either already exists or it was not created.", debug)
        
        try:
            os.mkdir(f'/home/pi/Desktop/{dataName}Data/Images/')
        except FileExistsError:
            printDebug("Directory Data/Images on desktop either already exists or it was not created.", debug)
        try:
            os.mkdir(f'/home/pi/Desktop/{dataName}Data/Audio/')
        except FileExistsError:
            printDebug("Directory Data/Audio on desktop either already exists or it was not created.", debug)
                        
        saveDir = '/home/pi/Desktop'
    
    ''' Setup the data '''
    # A: Audio
    # B: Temperature, Humidity, CPUTemperature, isThereMotion
    # C: Weight
    # D: Pictures
    
    fileDirImages = f'{saveDir}/{dataName}Data/Images'
    
    fileNameAudio = f'{saveDir}/{dataName}Data/Audio'
    headerAudio = ['Frequency', 'Amplitude'] # The time is in the name of the file

    fileNameTempHumCPUTempIsThereMot = f'{saveDir}/{dataName}Data/Data-A'
    headerTempHumCPUTempIsThereMot = ['Time', 'AirTemperature', 'AirHumidity', 'Motion', 'CPUTemp']

    fileNameWeight = f'{saveDir}/{dataName}Data/Data-B'
    headerWeight = ['Time', 'Weight']
 
    ''' Initialise the objects '''
    myCameras = Camera(fileDirImages, framerate, imageWidth, imageHeight, startTimeVideo, endTimeVideo, debug)
    mySensors = Sensors(debug, storageWarningThreshold, phoneNumbers, phoneNumbersKeys)
    myAudio = Audio(mySensors, sampRate, nameOfMicrophoneDevice, roundingAmountOfEachSample, debug)

    # Notify the user if it connected to WiFi successfully
    mySensors.sendMessage('Successfully initiated all 3 classes, and connected to the wifi.')
        
    ''' Set the Processes '''
    ''' Capture images and saves to specified path with a specified fps'''
    camerasProcess = Process(target = myCameras.captureImages, args=())

    ''' Capture sound and save '''
    audioProcess = Process(target = myAudio.recordAudio, args=(timeDurationAudio, headerAudio,
                                                           fileNameAudio, timeDurationAudio+5))

    ''' Capture rest of sensors '''
    sensorsProcess = Process(target = mySensors.saveSensorData, args=(headerTempHumCPUTempIsThereMot, headerWeight,
                                                                  fileNameTempHumCPUTempIsThereMot, fileNameWeight,
                                                                  timeIntervalTemperatureAndHumidity, timeIntervalWeight))

    ''' Start MultiProcessing '''
    
    camerasProcess.start()
    audioProcess.start()
    sensorsProcess.start()
    
    ''' Wait for each process to end and then continue on with the rest of the code '''
    camerasProcess.join()
    audioProcess.join()
    sensorsProcess.join()
  
        
except Exception as e:
    mySensors.closeAllSensors()
    myAudio.closeAllSensors()
    myCameras.closeAllCameras()
    printDebug("Closed from the exception in Controller.py, the next line is the error.", debug)
    printDebug(e, debug)

except KeyboardInterrupt:
    camerasProcess.terminate()
    audioProcess.terminate()
    sensorsProcess.terminate()
    mySensors.closeAllSensors()
    myAudio.closeAllSensors()
    myCameras.closeAllCameras()
    printDebug("KeyboardInterrupt caught in Controller.py", debug)
    
else:
    mySensors.closeAllSensors()
    myAudio.closeAllSensors()
    myCameras.closeAllCameras()
    printDebug("Closed from the else in Controller.py.", debug)
