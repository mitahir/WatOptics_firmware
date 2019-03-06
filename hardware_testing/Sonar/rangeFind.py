#!/usr/bin/python3
# Filename: rangeFind.py

# sample script to read range values from Maxbotix ultrasonic rangefinder

from time import sleep
import maxSonarTTY

def sonar_detect():
    serialPort = "/dev/ttyAMA0"
    maxRange = 5000  # change for 5m vs 10m sensor
    sleepTime = 1
    minMM = 9999
    maxMM = 0
    t = 0
    text_file = open("Sonar.txt", "w")
    while t<2:
        mm = maxSonarTTY.measure(serialPort)
        if mm >= maxRange:
            #print("no target")
            sleep(sleepTime)
            continue
        if mm < minMM:
            minMM = mm
        if mm > maxMM:
            maxMM = mm

        #print("distance:", mm, "  min:", minMM, "max:", maxMM)
        text_file.write(str(mm) + " ")
        
        sleep(1)
        t = t+1
    text_file.close()

sonar_detect()