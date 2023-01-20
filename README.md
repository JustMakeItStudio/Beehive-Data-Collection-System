# Data-Aquisition-System-Raspberry-pi-with-Python3
Collects temperature, humidity, sound, low frame rate video, and weight. These measurements are collected from a beehive and a camera trap.

### System required
* Raspberry pi 4
* Raspberry Pi OS 64 bit with Desktop


### How to use
Step 1. Get the raspberry updated, enable the camera, ssh, vnc, spi
```sh
sudo apt update
sudo apt upgrade
sudo pip3 install --upgrade setuptools
```
Step2. Install CircuitPython, you will be asked to switch to Python3 say yes, and after it's finished restart the device and continue from the next step
```sh
sudo pip3 install --upgrade adafruit-python-shell
wget https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/raspi-blinka.py
sudo python3 raspi-blinka.py
```
Step3. Install pipreqs (https://github.com/bndr/pipreqs) with
```sh
pip3 install pipreqs
```
Step4. Clone the directory to your pc with
```sh
git clone https://github.com/JustMakeItStudio/Beehive-Data-Collection-System
```
Step5. Install the dependencies with
*This doesn't work perfectly, it all came apart when I tried to install the pyaudio library
```sh
pip3 install -r requirements.txt
Still needs to be updated.
```

Step6. Run the Controller.py file
