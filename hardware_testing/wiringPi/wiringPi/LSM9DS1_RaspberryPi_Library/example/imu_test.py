#!/usr/bin/env python
# coding: utf-8

#import ctypes
from ctypes import *
import sys
import time
import numpy as np
from numpy import NaN, Inf, arange, isscalar, asarray, array

new_list = []
TIME_INTERVAL = 15
THRESHOLD = 0.375
path = "../lib/liblsm9ds1cwrapper.so"
lib = cdll.LoadLibrary(path)

lib.lsm9ds1_create.argtypes = []
lib.lsm9ds1_create.restype = c_void_p

lib.lsm9ds1_begin.argtypes = [c_void_p]
lib.lsm9ds1_begin.restype = None

lib.lsm9ds1_calibrate.argtypes = [c_void_p]
lib.lsm9ds1_calibrate.restype = None

lib.lsm9ds1_gyroAvailable.argtypes = [c_void_p]
lib.lsm9ds1_gyroAvailable.restype = c_int
lib.lsm9ds1_accelAvailable.argtypes = [c_void_p]
lib.lsm9ds1_accelAvailable.restype = c_int
lib.lsm9ds1_magAvailable.argtypes = [c_void_p]
lib.lsm9ds1_magAvailable.restype = c_int

lib.lsm9ds1_readGyro.argtypes = [c_void_p]
lib.lsm9ds1_readGyro.restype = c_int
lib.lsm9ds1_readAccel.argtypes = [c_void_p]
lib.lsm9ds1_readAccel.restype = c_int
lib.lsm9ds1_readMag.argtypes = [c_void_p]
lib.lsm9ds1_readMag.restype = c_int

lib.lsm9ds1_getGyroX.argtypes = [c_void_p]
lib.lsm9ds1_getGyroX.restype = c_float
lib.lsm9ds1_getGyroY.argtypes = [c_void_p]
lib.lsm9ds1_getGyroY.restype = c_float
lib.lsm9ds1_getGyroZ.argtypes = [c_void_p]
lib.lsm9ds1_getGyroZ.restype = c_float

lib.lsm9ds1_getAccelX.argtypes = [c_void_p]
lib.lsm9ds1_getAccelX.restype = c_float
lib.lsm9ds1_getAccelY.argtypes = [c_void_p]
lib.lsm9ds1_getAccelY.restype = c_float
lib.lsm9ds1_getAccelZ.argtypes = [c_void_p]
lib.lsm9ds1_getAccelZ.restype = c_float

lib.lsm9ds1_getMagX.argtypes = [c_void_p]
lib.lsm9ds1_getMagX.restype = c_float
lib.lsm9ds1_getMagY.argtypes = [c_void_p]
lib.lsm9ds1_getMagY.restype = c_float
lib.lsm9ds1_getMagZ.argtypes = [c_void_p]
lib.lsm9ds1_getMagZ.restype = c_float

lib.lsm9ds1_calcGyro.argtypes = [c_void_p, c_float]
lib.lsm9ds1_calcGyro.restype = c_float
lib.lsm9ds1_calcAccel.argtypes = [c_void_p, c_float]
lib.lsm9ds1_calcAccel.restype = c_float
lib.lsm9ds1_calcMag.argtypes = [c_void_p, c_float]
lib.lsm9ds1_calcMag.restype = c_float

def _datacheck_peakdetect(x_axis, y_axis):
    if x_axis is None:
        x_axis = range(len(y_axis))
    
    if len(y_axis) != len(x_axis):
        raise ValueError( 
                "Input vectors y_axis and x_axis must have same length")
    
    #needs to be a numpy array
    y_axis = np.array(y_axis)
    x_axis = np.array(x_axis)
    return x_axis, y_axis


def peakdet(v, delta, x = None):
    """
    Converted from MATLAB script at http://billauer.co.il/peakdet.html
    
    Returns two arrays
    
    function [maxtab, mintab]=peakdet(v, delta, x)
    %PEAKDET Detect peaks in a vector
    %        [MAXTAB, MINTAB] = PEAKDET(V, DELTA) finds the local
    %        maxima and minima ("peaks") in the vector V.
    %        MAXTAB and MINTAB consists of two columns. Column 1
    %        contains indices in V, and column 2 the found values.
    %      
    %        With [MAXTAB, MINTAB] = PEAKDET(V, DELTA, X) the indices
    %        in MAXTAB and MINTAB are replaced with the corresponding
    %        X-values.
    %
    %        A point is considered a maximum peak if it has the maximal
    %        value, and was preceded (to the left) by a value lower by
    %        DELTA.
    
    % Eli Billauer, 3.4.05 (Explicitly not copyrighted).
    % This function is released to the public domain; Any use is allowed.
    
    """
    maxtab = []
    mintab = []
       
    if x is None:
        x = arange(len(v))
    
    v = asarray(v)
    
    if len(v) != len(x):
        sys.exit('Input vectors v and x must have same length')
    
    if not isscalar(delta):
        sys.exit('Input argument delta must be a scalar')
    
    if delta <= 0:
        sys.exit('Input argument delta must be positive')
    
    mn, mx = Inf, -Inf
    mnpos, mxpos = NaN, NaN
    
    lookformax = True
    
    for i in arange(len(v)):
        this = v[i]
        if this > mx:
            mx = this
            mxpos = x[i]
        if this < mn:
            mn = this
            mnpos = x[i]
        
        if lookformax:
            if this < mx-delta:
                maxtab.append((mxpos, mx))
                mn = this
                mnpos = x[i]
                lookformax = False
        else:
            if this > mn+delta:
                mintab.append((mnpos, mn))
                mx = this
                mxpos = x[i]
                lookformax = True

    return array(maxtab), array(mintab)




    #from matplotlib.pyplot import plot, scatter, show
def imu_step_counter(num_steps):
	imu = lib.lsm9ds1_create()
	lib.lsm9ds1_begin(imu)
	if lib.lsm9ds1_begin(imu) == 0:
		print("Failed to communicate with LSM9DS1.")
		quit()
	lib.lsm9ds1_calibrate(imu)
	start_time = time.time()
	counter = 0
	data_list = []
	#num_steps = 0

	print("Start walking")
	while True:
		counter+=1
		
		while lib.lsm9ds1_gyroAvailable(imu) == 0:
			pass
		lib.lsm9ds1_readGyro(imu)
		while lib.lsm9ds1_accelAvailable(imu) == 0:
			pass
		lib.lsm9ds1_readAccel(imu)
		while lib.lsm9ds1_magAvailable(imu) == 0:
			pass
		lib.lsm9ds1_readMag(imu)

		gx = lib.lsm9ds1_getGyroX(imu)
		gy = lib.lsm9ds1_getGyroY(imu)
		gz = lib.lsm9ds1_getGyroZ(imu)

		ax = lib.lsm9ds1_getAccelX(imu)
		ay = lib.lsm9ds1_getAccelY(imu)
		az = lib.lsm9ds1_getAccelZ(imu)

		mx = lib.lsm9ds1_getMagX(imu)
		my = lib.lsm9ds1_getMagY(imu)
		mz = lib.lsm9ds1_getMagZ(imu)

		cgx = lib.lsm9ds1_calcGyro(imu, gx)
		cgy = lib.lsm9ds1_calcGyro(imu, gy)
		cgz = lib.lsm9ds1_calcGyro(imu, gz)

		cax = lib.lsm9ds1_calcAccel(imu, ax)
		cay = lib.lsm9ds1_calcAccel(imu, ay)
		caz = lib.lsm9ds1_calcAccel(imu, az)

		cmx = lib.lsm9ds1_calcMag(imu, mx)
		cmy = lib.lsm9ds1_calcMag(imu, my)
		cmz = lib.lsm9ds1_calcMag(imu, mz)

	   # print("Gyro: %f, %f, %f [deg/s]" % (cgx, cgy, cgz))
		#print("Accel: %f, %f, %f [Gs]" % (cax, cay, caz))
	   # print("Mag: %f, %f, %f [gauss]" % (cmx, cmy, cmz))
		data_list.append(cay)
		new_list.append(cay)
		end_time = time.time()
		
		
		
		# if(end_time-start_time > 2):
				# print (counter)
				# break
		
		if(end_time-start_time >= 20):
			break
		

		if(counter >= 125):
			print(num_steps)
			print("\n")
	
			maxpeak = max(data_list)
			minpeak = min(data_list)
			if((maxpeak-minpeak) >=0.10):
				num_steps+=1
			

			#plot(data_list)
	   
			#maxtab, mintab = peakdet(data_list,THRESHOLD) #need to play around with this threshold value
			#num_steps+= len(maxtab) + len(mintab)
			#scatter(array(maxtab)[:,0], array(maxtab)[:,1], color='blue')
			#scatter(array(mintab)[:,0], array(mintab)[:,1], color='red')
			#show()
			#print("STEPS: " + str(num_steps))
			#print("Positive: " , maxtab)
			#print("Negative: ", mintab)
			
			#print (counter)
			data_list = [] 
			counter = 0
			
	#print(num_steps)
	#plot(new_list)
	#show()
			
	#sys.exit(0)
	
imu_step_counter(0)
	
