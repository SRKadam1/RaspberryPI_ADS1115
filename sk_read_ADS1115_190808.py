# Script takes ~2 (1.9) seconds to import & setup.
# It is best to wait until "Setup complete" is received before starting 1st microcontroller.

# IMPORTS
import time
import RPi.GPIO as GPIO
from Adafruit_ADS1x15 import ADS1115
import numpy as np
import os
import sys

# SETUP

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
# LED Pin 
#LEDPIN = 18
#GPIO.setup(LEDPIN,GPIO.OUT)
#GPIO.output(LEDPIN,0)
# 1st mirocontroller communication
# assumption: when 1st micrcontroller starts process, it will send a continuous HIGH signal to the 2nd microcontroller.
ReadDigitalPin = 15
GPIO.setup(ReadDigitalPin,GPIO.IN)
# Event parameters
running = False
raw_data = False
# ADS1115 ADC (16-bit) instance
adc = ADS1115()
GAIN = 1
# "samples per second" (ADC's conversion time = 1/sps)
# does not change internal sampling rate [lower sps = more data averaged per sample]
sps = 860
# Data storage
data = []
# Paths
rpi_specific_path = "/home/pi/ADC/data"
print("Setup complete")

# LOOP
while True:
	try:
		# While pin is HIGH...
		while GPIO.input(ReadDigitalPin)==1:
			# If printer hasn't started job...
			if running == False:
				timestr_csv = time.strftime("%Y%m%d-%H%M%S") + ".csv" 
				adc.start_adc_difference(0, gain=GAIN, data_rate=sps)
				#GPIO.output(LEDPIN,1)
				running = True
			# If printer currently in job...
			if running == True:
				data.append( (time.time(), adc.get_last_result()) )

		# While pin is LOW...
		while GPIO.input(ReadDigitalPin)==0:
			# If printer just finished job...
			if running == True:
				adc.stop_adc()
				#GPIO.output(LEDPIN,0)
				raw_data = True
				running = False
			# If printer not printing....
			if running == False:
				# If printer completed job...
				if raw_data == True:
					# Process data.
					data = np.asarray(data)
					time_offset = data[0][0]
					print("process data")
					for data_point in data:
						data_point[0] = data_point[0] - time_offset
					print("len(data): ", len(data))
					print("First datapoint (sec,ADC): ", data[0])
					print("Last datapoint (sec,ADC): ", data[-1])
					# Save data.
					timestr_dir = time.strftime("%Y%m%d")
					dir_path = os.path.join(rpi_specific_path, timestr_dir)
					csv_path = os.path.join(dir_path,timestr_csv)
					if not os.path.exists(dir_path):
						os.makedirs(dir_path)
						print("Created new directory ", dir_path)
					print("saving data...")
					np.savetxt(csv_path, data, delimiter=',')
					print("Saved data to ", csv_path)
					raw_data = False
					data = []
				# If printer hasn't started job... wait for HR3
		time.sleep(0.0008)
		print("collect data")

	# If printer needs to be stopped...
	except KeyboardInterrupt:
		adc.stop_adc()
		#GPIO.output(LEDPIN,0)
		print("\n MANUAL STOP SUCCESSFUL \n")
		# If printer in job...
		if running == True:
			data = np.asarray(data)
			time_offset = data[0][0]
			print("process data")
			for data_point in data:
				data_point[0] = data_point[0] - time_offset
			print("len(data): ", len(data))
			print("First datapoint (sec,ADC): ", data[0])
			print("Last datapoint (sec,ADC): ", data[-1])
			# Save data.
			timestr_dir = time.strftime("%Y%m%d")
			dir_path = os.path.join(rpi_specific_path, timestr_dir)
			csv_path = os.path.join(dir_path,timestr_csv)
			if not os.path.exists(dir_path):
				os.makedirs(dir_path)
				print("Created new directory ", dir_path)
			np.savetxt(csv_path, data, delimiter=',')
			print("Saved data to ", csv_path)
			# Precaution (script will redefine these variables when rerun)
			raw_data = False
			data = []
			running = False
		break
