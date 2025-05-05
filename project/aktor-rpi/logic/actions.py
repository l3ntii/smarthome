import RPi.GPIO as GPIO
import config
import state
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(config.PIN_LIGHT, GPIO.OUT)
GPIO.setup(config.PIN_HEAT, GPIO.OUT)
GPIO.setup(config.PIN_FAN, GPIO.OUT)
GPIO.setup(config.PIN_BUZZER, GPIO.OUT)

fan_pwm = GPIO.PWM(config.PIN_FAN, 50)
fan_pwm.start(0)

buzzer_pwm = GPIO.PWM(config.PIN_BUZZER, 1000)

def set_light(on):
    GPIO.output(config.PIN_LIGHT, on)

def set_heat(on):
    GPIO.output(config.PIN_HEAT, on)

def set_buzzer(on):
    import RPi.GPIO as GPIO
    GPIO.output(config.PIN_BUZZER, on)

def set_fan(on):
    if on:
        fan_pwm.ChangeDutyCycle(7.5)
    else:
        fan_pwm.ChangeDutyCycle(0)

def buzzer_on():
    buzzer_pwm.start(50)

def buzzer_off():
    buzzer_pwm.stop()

def cleanup():
    fan_pwm.stop()
    buzzer_pwm.stop()
    GPIO.cleanup()