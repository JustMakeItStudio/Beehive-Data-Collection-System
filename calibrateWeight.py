import os
import sys
from HX711 import *


try:
    hx = SimpleHX711(22, 27, 1, 0)
except GpioException:
    print("Failed to connect to HX711 chip", file=sys.stderr)
    sys.exit(os.EX_UNAVAILABLE)
except TimeoutException:
    print("Failed to connect to HX711 chip", file=sys.stderr)
    sys.exit(os.EX_UNAVAILABLE)


print("""
\x1B[2J\x1B[H
========================================
HX711 Calibration
========================================
Find an object you know the weight of. If you can't find anything,
try searching Google for your phone's specifications to find its weight.
You can then use your phone to calibrate your scale.
""")

unit = input("1. Enter the unit you want to measure the object in (eg. g, kg, lb, oz): ")

knownWeight = float(input("2. Enter the weight of the object in the unit you chose (eg. " +
                    "if you chose 'g', enter the weight of the object in grams): "))

samples = int(input("3. Enter the number of samples to take from the HX711 chip (eg. 15): "))

input("4. Remove all objects from the scale and then press enter.")
print("Working...")

zeroValue = hx.read(Options(int(samples)))

input("5. Place object on the scale and then press enter.")
print("Working...")

raw = hx.read(Options(int(samples)))
refUnitFloat = (raw - zeroValue) / knownWeight
refUnit = round(refUnitFloat, 0)

if refUnit == 0:
    refUnit = 1

print(
    "\n\n" +
    "Known weight (your object) " + str(knownWeight) + " " + unit + "\n" +
    "Raw value over " + str(samples) + " samples: " + str(raw) + "\n" +
    "\n" +
    "-> REFERENCE UNIT: " + str(round(refUnit)) + "\n" +
    "-> ZERO VALUE: " + str(round(zeroValue)) + "\n" +
    "\n" +
    "You can provide these values to the constructor when you create the "
    "HX711 objects or later on. For example: \n" +
    "\n" +
    "hx = SimpleHX711(" + '22' + ", " + '27' + ", " + 
    str(round(refUnit)) + ", " + str(round(zeroValue)) + ")\n" +
    "OR\n" +
    "hx.setReferenceUnit(" + str(round(refUnit)) + ") and " +
    "hx.setOffset(" + str(round(zeroValue)) + ")\n"
)

sys.exit(os.EX_OK)