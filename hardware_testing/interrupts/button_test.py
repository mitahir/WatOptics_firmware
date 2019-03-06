import RPi.GPIO as GPIO
import sys
import time
import subprocess
 
GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 16 to be an input pin and set initial value to be pulled low (off)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 18 to be an input pin and set initial value to be pulled low (off)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 22 to be an input pin and set initial value to be pulled low (off)
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 24 to be an input pin and set initial value to be pulled low (off)

thousands = 4
hundreds = 0
tens = 0
ones = 0


while True: # Run forever
    if GPIO.input(16) == GPIO.HIGH:
        
        #roomNumber = 4008
        
        hundreds += 1
        if (hundreds > 9):
            hundreds = 0
        subprocess.call(["espeak", str(hundreds)])
        time.sleep(0.3)
        
    if GPIO.input(18) == GPIO.HIGH:
        
        #roomNumber = 4037
        
        tens += 1
        if (tens > 9):
            tens = 0
        subprocess.call(["espeak", str(tens)])
        time.sleep(0.3)
        
    if GPIO.input(22) == GPIO.HIGH:
        
        #roomNumber = 4032
        
        ones += 1
        if (ones > 9):
            ones = 0
        subprocess.call(["espeak", str(ones)])
        time.sleep(0.3)
    
    if GPIO.input(24) == GPIO.HIGH:
    
        #roomNumber = 4118
    
        print("EXIT BUTTON")
        break
			
roomNumber = (thousands * 1000) + (hundreds * 100) + (tens * 10) + ones

thousand_s = str(thousands) + ' '
hundred_s = str(hundreds) + ' '
ten_s = str(tens) + ' '
one_s = str(ones) + ' '

roomNumber_s = thousand_s + hundred_s + ten_s + one_s

subprocess.call(["espeak", roomNumber_s])

print(roomNumber)
            
sys.exit(0)         