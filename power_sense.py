# Import the required module. 
import RPi.GPIO as GPIO 
import time


# Set the mode of numbering the pins.
GPIO.setmode(GPIO.BOARD) 

# GPIO pin 10 is the output.
# GPIO.setup(10, GPIO.OUT)
# GPIO pin 8 is the input.
GPIO.setup(6, GPIO.IN)

# # Initialise GPIO10 to high (true) so that the LED is off.
# GPIO.output(10, True)
# while 1:
#     if GPIO.input(8):
#         GPIO.output( 10, False)
#     else:
#         # When the button switch is not pressed, turn off the LED.
#         GPIO.output( 10, True)


def outlet_powered():
    return GPIO.input(6)


while True:
    print outlet_powered()
    time.sleep(1)
