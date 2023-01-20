# Audio handling class
import pyaudio #  sudo apt-get install python3-pyaudio
import numpy as np # pip3 install numpy==1.16.2
import time
from Sensor import Sensors
import os

class Audio:
    
    def __init__(self, sensorObject: object, sampRate: int, nameOfMicrophoneDevice: str, roundingAmountOfEachSample: int, debug: bool):
        self.debug = debug
        self.audioSensor = self.initAudioSensor()
        self.mySave = sensorObject
        self.sampRate = sampRate # 44.1kHz sampling rate
        self.number = 1
        self.nameOfMicrophoneDevice = nameOfMicrophoneDevice
        self.roundingAmountOfEachSample = roundingAmountOfEachSample
        
    def getAudioSensor(self):
        return self.audioSensor
    
    def getIndexOfConnectedAudioDevices(self, audioObject, searchFor: str):
        for i in range(audioObject.get_device_count()):
            if searchFor in audioObject.get_device_info_by_index(i).get('name'):
                self.printDebug(f'Found the audio device specified {i}', self.debug)
                return i
        self.printDebug("Couldn't find the audio device specified", self.debug)
        return None
             
    def initAudioSensor(self):
        # The first microphone: GEMBIRD MIC-C-01 CLIP-ON 3.5 MM
        # {
        #   Frequency response: 20Hz - 16kHz
        #   Sensitivity: -42dB+-2dB
        #   Output impetance: > 2.2k Ohm
        # } 
        # The new microphone: BOYA BY-MC2 USB Microphone
        # {
        #   Frequency response: 35Hz - 18kHz
        #   Sensitivity: -47dB+/-1dB/0dB=1V/Pa,1kHz
        #   Output impetance: 300 Ohm
        # }
        audioObject = pyaudio.PyAudio() # create pyaudio instantiation
        return audioObject
    
#-------------------------------------------------------------------------------------
    def recordAudio(self, recordingDuration: int, header: list, fileName: str, functionDuration: int):
        # recordingDuration in seconds
        audioVariableFormat = pyaudio.paInt16 # 16-bit resolution
        recordingChannels = 1 # 1 channel
        chunk = 4096 # 2^12 samples for buffer
        microphoneDeviceIndex = self.getIndexOfConnectedAudioDevices(self.audioSensor, 'PDP Audio Device')
        microphoneSensitivitydBV = -47.0
        if microphoneDeviceIndex is None:
            microphoneDeviceIndex = self.getIndexOfConnectedAudioDevices(self.audioSensor, self.nameOfMicrophoneDevice) # device index found by p.get_device_info_by_index(ii)
            # mic sensitivity correction and bit conversion
            microphoneSensitivitydBV = -42.0 # mic sensitivity in dBV + any gain
        mic_sens_corr = np.power(10.0,microphoneSensitivitydBV/20.0) # calculate mic sensitivity conversion factor
        
        while 1:
            recordingName = time.strftime("%Y_%m_%d-%H%M%S")
            recordingFileName = time.strftime("%Y_%m_%d")
            
            stream = self.audioSensor.open(format=audioVariableFormat,
                                rate=self.sampRate,
                                channels=recordingChannels,
                                input_device_index=microphoneDeviceIndex,
                                input=True,
                                frames_per_buffer=chunk
                               )

            frames = []
            startTime = time.time() # this doesnt need to be the actual time, it is just a time reference
            for i in range(0, int((self.sampRate/chunk)*recordingDuration)):
                data = np.frombuffer(stream.read(chunk, exception_on_overflow = False), 'int16')
                data = ((data/np.power(2.0,15))*5.25)*(mic_sens_corr)
                frames.extend(data)
            
            stream.stop_stream()
            stream.close()

            # Rounnd each individual sample (tihs is about 3 orders of magnitude faster than using the round function in a for loop)
            roundedFrames = np.around(frames, self.roundingAmountOfEachSample)

            fourieredFrames = self.doFourierTransform(roundedFrames)
            # Each time a recording is made, save the frequency domain to a new csv file.
            try:
                os.mkdir(f'{fileName}/{recordingFileName}/')
            except:
                pass
            finalFileName = f'{fileName}/{recordingFileName}/{recordingName}'
            # fourieredFrames = [frequency, amplitude]
            self.mySave.writeDataToCSV(header, fourieredFrames, finalFileName)
            self.number += 1
            
            restingTime = functionDuration - (time.time()-startTime)
            if restingTime < 0:
                restingTime = 0
                self.printDebug('I need more time!', self.debug)
            time.sleep(restingTime)
           
        
    def doFourierTransform(self, samples: list, numberOfFrequenciesToReturn=5):  
        # Documentation 1: https://numpy.org/doc/stable/reference/generated/numpy.fft.fft.html
        # Documentation 2: https://pythontic.com/visualization/signals/fouriertransform_fft
        fourierTransform = np.fft.fft(samples)/len(samples)           # Normalize samples
        # Get the important info from the imaginary part and round the numpy array
        fourierTransform = np.around(abs(fourierTransform[range(int(len(samples)/2))]), 5) # Exclude sampling frequency
        tpCount = len(samples)
        values = np.arange(int(tpCount/2))
        timePeriod = tpCount/self.sampRate
        frequencies = np.around(values/timePeriod, 2)
        return [frequencies, fourierTransform] # returns the frequencies and the corresponding amplitude
    
    def printDebug(self, msg: str, debug: bool):
        if debug:
            print(f'Debug: {msg}')
            with open('debug.txt', 'a') as f:
                f.write(f'{time.strftime("%Y_%m_%d-%H%M%S")} {msg}')
                f.write('\n')
        
    ### Close everything before shutting down the program ###
    def closeAllSensors(self):
        self.audioSensor.terminate()



