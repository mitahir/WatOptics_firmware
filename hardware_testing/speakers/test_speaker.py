#!/usr/bin/env python2

import RPi.GPIO as GPIO
import time
import sys

def note_to_freq(note,a=440.0):
	notes = { 'a':9,
		'b':11,
		'c':0,
		'd':2,
		'e':4,
		'f':5,
		'g':7,
		}
	c = a * (2**(1/12.0))**(-57) # c0

	f = notes[note[0]]

	if "is" in note:
		f += 1
		n = int(note[3:])
	elif "es" in note:
		f -= 1
		n = int(note[3:])
	else:
		n = int(note[1:])

	return c * (2**(1/12.0))**(f+(n*12))

def init():
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(23, GPIO.OUT)

def sound(length, freq):
	i = 1.0/freq
	fut = time.time() + length
	while time.time() < fut:
		now = time.time()
		GPIO.output(23, GPIO.HIGH)
		GPIO.output(23, GPIO.LOW)
		time.sleep(i - 0.00018)

def play(music,user_a):
	T = 240 / float(music.pop(0)) # time in seconds for a bar
	for note in music:
		if note[0] != '/':
			c = note.index(" ")
			freq = note_to_freq(note[:c],a=user_a)
			length = T/float(note[c+1:])
			sound(length, freq)

if __name__ == "__main__":
	init()
	music = open(sys.argv[1]).read().split("\n")
	music.pop()
	if "-a" in sys.argv:
		a = float(sys.argv[sys.argv.index("-a")+1])
	else:
		a = 440
	play(music,a)
