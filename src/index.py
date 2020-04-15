import distutils.util
import time
import numpy as np
import RPi.GPIO as GPIO

from src.file_paths import PathConsts


class Backlighting:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)

        # LED GPIO SETUP
        self.red_color_channel = 2
        self.green_color_channel = 3
        self.blue_color_channel = 4

        GPIO.setup(self.red_color_channel, GPIO.OUT)
        GPIO.setup(self.green_color_channel, GPIO.OUT)
        GPIO.setup(self.blue_color_channel, GPIO.OUT)

        Freq = 255

        self.RED = GPIO.PWM(self.red_color_channel, Freq)
        self.GREEN = GPIO.PWM(self.green_color_channel, Freq)
        self.BLUE = GPIO.PWM(self.blue_color_channel, Freq)

        # MICRO GPIO SETUP
        self.micro_channel = 9
        GPIO.setup(self.micro_channel, GPIO.IN)

        # BUTTON GPIO SETUP
        self.button_channel = 17
        GPIO.setup(self.button_channel, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        self.is_on = False

        self.default_color = [50, 50, 50]

    def led_off(self):
        self.change_color([0, 0, 0])
        self.is_on = False

    def led_on(self):
        self.change_color(self.default_color)
        self.is_on = True

    def change_led_state(self):
        if self.is_on:
            self.led_off()
        else:
            self.led_on()

    def change_color(self, color):
        self.RED.start(color[0])
        self.GREEN.start(color[1])
        self.BLUE.start(color[2])

    @staticmethod
    def create_random_color():
        return [np.random.randint(0, 100), np.random.randint(0, 100), np.random.randint(0, 100)]

    def change_to_random_color(self):
        color = self.create_random_color()
        self.change_color(color)

    # on/off according to data received from web (mqtt)
    def change_led_state_from_file(self, led_state_file):
        state = open(led_state_file, mode="r", encoding="utf-8").readline()
        self.is_on = distutils.util.strtobool(state)
        self.change_led_state()

    # change color according to data received from web (mqtt)
    def change_color_from_file(self, color_state_file):
        color = open(color_state_file, mode="r", encoding="utf-8").readline()
        color = color.split(" ")
        self.default_color = color
        self.change_color(self.default_color)

    def exec(self):
        try:
            while True:
                self.change_led_state_from_file(PathConsts.state_filename)
                self.change_color_from_file(PathConsts.color_filename)

                if not GPIO.input(self.button_channel):
                    print('color')
                    self.change_to_random_color()
                    time.sleep(0.5)
                elif GPIO.input(self.micro_channel) == 1:
                    print('state')
                    self.change_led_state()
                    time.sleep(0.5)
        except KeyboardInterrupt:
            GPIO.cleanup()


Backlighting().exec()
