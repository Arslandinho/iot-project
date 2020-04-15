import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

delayTime = 0.5

Button_PIN = 17
GPIO.setup(Button_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

try:
    while True:
        if GPIO.input(Button_PIN):
            print("Button: not pushed")
        else:
            print("Button: pushed")

        button_pressed = False
        time.sleep(delayTime)
except KeyboardInterrupt:
    GPIO.cleanup()
