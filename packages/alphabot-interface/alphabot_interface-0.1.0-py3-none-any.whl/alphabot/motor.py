import RPi.GPIO as GPIO
import time

class Motor:
    def __init__(self, ain1=12, ain2=13, ena=6, bin1=20, bin2=21, enb=26):
        self.AIN1 = ain1
        self.AIN2 = ain2
        self.BIN1 = bin1
        self.BIN2 = bin2
        self.ENA = ena
        self.ENB = enb

        self.speed_calibration = 1.0
        self.angle_calibration = 1.0

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.AIN1, GPIO.OUT)
        GPIO.setup(self.AIN2, GPIO.OUT)
        GPIO.setup(self.BIN1, GPIO.OUT)
        GPIO.setup(self.BIN2, GPIO.OUT)
        GPIO.setup(self.ENA, GPIO.OUT)
        GPIO.setup(self.ENB, GPIO.OUT)

        self.pwmA = GPIO.PWM(self.ENA, 500)
        self.pwmB = GPIO.PWM(self.ENB, 500)
        self.pwmA.start(0)
        self.pwmB.start(0)

        self.stop()

    def forward(self, speed, angle=0):
        speed = max(0, min(100, speed)) * self.speed_calibration
        angle = max(-100, min(100, angle)) * self.angle_calibration

        left_speed = speed
        right_speed = speed

        if angle > 0:
            right_speed *= (1 - abs(angle) / 100)
        elif angle < 0:
            left_speed *= (1 - abs(angle) / 100)

        self.set_motor(left_speed, right_speed)

    def backward(self, speed, angle=0):
        speed = max(0, min(100, speed)) * self.speed_calibration
        angle = max(-100, min(100, angle)) * self.angle_calibration

        left_speed = -speed
        right_speed = -speed

        if angle > 0:
            right_speed *= (1 - abs(angle) / 100)
        elif angle < 0:
            left_speed *= (1 - abs(angle) / 100)

        self.set_motor(left_speed, right_speed)

    def look_around(self, speed=50, duration=2):
        """
        Rotates the robot in place to scan surroundings.
        """
        speed = max(0, min(100, speed)) * self.speed_calibration
        self.set_motor(-speed, speed)  # Left motor backward, right motor forward
        time.sleep(duration)
        self.stop()

    def set_motor(self, left_speed, right_speed):
        if right_speed >= 0:
            GPIO.output(self.AIN1, GPIO.LOW)
            GPIO.output(self.AIN2, GPIO.HIGH)
        else:
            GPIO.output(self.AIN1, GPIO.HIGH)
            GPIO.output(self.AIN2, GPIO.LOW)
        self.pwmA.ChangeDutyCycle(min(abs(right_speed), 100))

        if left_speed >= 0:
            GPIO.output(self.BIN1, GPIO.LOW)
            GPIO.output(self.BIN2, GPIO.HIGH)
        else:
            GPIO.output(self.BIN1, GPIO.HIGH)
            GPIO.output(self.BIN2, GPIO.LOW)
        self.pwmB.ChangeDutyCycle(min(abs(left_speed), 100))

    def stop(self):
        self.pwmA.ChangeDutyCycle(0)
        self.pwmB.ChangeDutyCycle(0)
        GPIO.output(self.AIN1, GPIO.LOW)
        GPIO.output(self.AIN2, GPIO.LOW)
        GPIO.output(self.BIN1, GPIO.LOW)
        GPIO.output(self.BIN2, GPIO.LOW)

    def set_speed_calibration(self, factor):
        self.speed_calibration = factor

    def set_angle_calibration(self, factor):
        self.angle_calibration = factor