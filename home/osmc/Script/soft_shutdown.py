import RPi.GPIO as GPIO
import os
from time import sleep

PIN_LED = 13
PIN_BTN = 11
BOUNCE_DELAY = 3000


# Shutdown interrupt callback
def shutdown(pin):
    GPIO.remove_event_detect(PIN_BTN)
    sleep(0.3)
    
    # Blink the led
    for i in range(5):
        GPIO.output(PIN_LED, GPIO.LOW)
        sleep(0.1) 
        GPIO.output(PIN_LED, GPIO.HIGH)
        sleep(0.1) 
 
    # Then shutdown the pi!
    os.system("sudo shutdown -h now")


GPIO.setmode(GPIO.BOARD)
GPIO.setup(PIN_LED, GPIO.OUT, initial=GPIO.HIGH) # Power led ON at boot
GPIO.setup(PIN_BTN, GPIO.IN, pull_up_down = GPIO.PUD_UP)

# Wait several seconds until pi boot up
sleep(10)

# Add interrupt for the shutdown button
GPIO.add_event_detect(PIN_BTN, GPIO.RISING, callback=shutdown, bouncetime=BOUNCE_DELAY)

while True:
    # sleep to reduce unnecessary CPU usage
    sleep(5)
