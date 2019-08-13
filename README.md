# RaspberryPI_ADS1115

This Python (not CircuitPython) code is intended for collecting Analog-to-Digital Converter (ADC) counts with a timestamp. 

The Raspberry Pi will collect data and save to a csv file as long as it receives a HIGH signal. The code is cyclic; once it has been started from the terminal or command line, it will repeat the process of waiting, collecting data, and storing data until interrupted. 

## Equipment 

- This code was written on a [Raspberry Pi 0W](https://www.raspberrypi.org/products/raspberry-pi-zero-w/) but can be run on any Raspberry Pi. 


- The [ADS1115](https://www.adafruit.com/product/1085) is a 16-bit, general-pupose, programmble gain amplifier (PGA) ADC breakboard board from Adafruit & Texas Instruments ([datasheet](https://cdn-shop.adafruit.com/datasheets/ads1115.pdf)).


- This code uses [Adafruit's ADS1115 Python library](https://github.com/adafruit/Adafruit_Python_ADS1x15). 

## Setup
The microcontroller-ADC wiring is described in [Adafruit's tutorial](https://learn.adafruit.com/raspberry-pi-analog-to-digital-converters/ads1015-slash-ads1115). 

This code assumes __two__ microcontrollers. The first is controlling some process which produces analog measurements. The second is a Raspberry Pi communicating with the ADS1115 chip. Since both mirocontrollers control events on independent timelines, timestamps are created to correlate the two chronologies. 

## Use
### Sampling Rate  
Generally, this code returns 820 samples per second. The ADS1115 datasheet sets an upper limit of 860 samples per second. While the Raspberry Pi's bus speed can be changed from the default 100000 to 400000 ((https://www.raspberrypi-spy.co.uk/2018/02/change-raspberry-pi-i2c-bus-speed/)), doing so does not positively impact the sampling rate of the afore-described setup. It results in ADC data being read by the Raspberry Pi multiple times (data duplication). 

If you are willing to trade precision for speed, the [ADS1015](https://www.adafruit.com/product/1083) is a 12-bit ADC with an upper limit of 3,300 samples per second.

## Notes  
Please see the examples in [Adafruit's ADS1115 Python library](https://github.com/adafruit/Adafruit_Python_ADS1x15) for explanations on how to alter I2C addresses, ADC conversion speeds, PGA, etc.

A detailed explanation of I2C is provided in the [ADS1115 datasheet](https://cdn-shop.adafruit.com/datasheets/ads1115.pdf), but a nice job of explaining I2C and its relevance to microcontroller-ADS1115 communication and code can also be found [here](http://openlabtools.eng.cam.ac.uk/Resources/Datalog/RPi_ADS1115/).

If you are interested in using CircuitPython or Arduino, check out [Adafruit's newer tutorial](https://learn.adafruit.com/adafruit-4-channel-adc-breakouts/).
