import time
import requests
import dweepy
import ADC0832
import math
import threading
import RPi.GPIO as GPIO

# GPIO and thing configuration
LED_PIN = 5							# GPIO pin where the LED is connected
myThing = "Gonzalo_Raspi_9909"		# Replace with you OWN thing name
key1 = "temperature"
n = 15 								# Start the counter

# Initialize ADC0832 and GPIO
def init():
	ADC0832.setup()
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(LED_PIN, GPIO.OUT)
	GPIO.output(LED_PIN, GPIO.LOW)

# Read temperature from thermistor
def get_temperature():
	res = ADC0832.getADC(0)		 
	if float(res) == 1:
		celsius = 23.00
	else:	
		Vr = 3.3 * float(res) / 255
		Rt = 10000 * ((255 / float(res)) - 1)
		temp = 1/(((math.log(Rt / 10000)) / 3380) + (1 / (273.15 + 25)))
		celsius = round(temp - 273.15, 2)
	return celsius

# Main data publishing loop
def main_loop():
	count = n
	while count > 0:
		celsius = get_temperature()
		dweepy.dweet_for(myThing, {key1: str(celsius)})
		print ('Celsius: %.2f C' % (celsius))
		time.sleep(5)
		count -= 1

# Control LED based on the temperature
def led_control_listener():
	for dweet in dweepy.listen_for_dweets_from(myThing):
		if key1 in dweet['content']:
			celsius = dweet['content'][key1]
			if celsius < 28:
				GPIO.output(LED_PIN, GPIO.HIGH)
				print('LED OFF')
			else:
				GPIO.output(LED_PIN, GPIO.LOW)
				print('LED ON')

# Setup and start
if __name__ == '__main__':
	init()
	try:
		t1 = threading.Thread(target=main_loop)
		t1.start()
		
		led_control_listener()
	except KeyboardInterrupt:
		ADC0832.destroy()
		GPIO.cleanup()
		print("Program ended")
