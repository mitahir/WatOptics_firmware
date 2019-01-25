# This is an example program to show how to generate speech with the RaspberryPi.  
# You can see the full written tutorial here:  http://www.dexterindustries.com/howto/make-your-raspberry-pi-speak/
# This program makes the Pi speak aloud the text entered by the user and it also records it to a file named Textwav.

import subprocess
import sys

varText = sys.argv[1]

subprocess.call(["espeak", varText])

