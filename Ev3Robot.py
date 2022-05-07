#!/usr/bin/env pybricks-micropython
import socket
import threading
import time

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile


HOST = '192.168.194.1'
PORT = 42422  # Port to listen on (non-privileged ports are > 1023)

# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.
ev3 = EV3Brick()
# Initialize the motors.
left_motor = Motor(Port.B)
right_motor = Motor(Port.C)

# Initialize the color sensor.
light = ColorSensor(Port.S3)
us = UltrasonicSensor(Port.S4)

# Initialize the drive base.
ev3 = EV3Brick()
robot = DriveBase(left_motor, right_motor, wheel_diameter=55.5, axle_track=104)

# Calculate the light threshold. Choose values based on your measurements.
BLACK = 6
WHITE = 56
# RED = 64
# YELLOW = 84
# BLUE = 13
# GREEN = 10
threshold = (BLACK + WHITE) / 2

# Set the drive speed at 100 millimeters per second.
DRIVE_SPEED = 50

# Set the gain of the proportional line controller. This means that for every
# percentage point of light deviating from the threshold, we set the turn
# rate of the drivebase to 1.2 degrees per second.

# For example, if the light value deviates from the threshold by 10, the robot
# steers at 10*1.2 = 12 degrees per second.
PROPORTIONAL_GAIN = 2.0

is_auto_mode = False


def go_left():
    # TODO: command the robot to go (turn) left
    robot.drive(0, -50)


def go_right():
    # TODO: command the robot to go (turn) left
    robot.drive(0, 50)


def go_forward():
    # TODO: command the robot to go forward
    robot.drive(50, 0)


def go_backward():
    # TODO: command the robot to go backward
    robot.drive(-50, 0)


def stop():
    is_auto_mode = False
    robot.stop()


def stop_wait():
    while us.distance() < 100:
        robot.stop()
        wait(10)


def auto_mode():
    # TODO: Auto mode instruction
    is_auto_mode = True
    while is_auto_mode:
        # Calculate the deviation from the threshold.
        deviation = light.reflection() - threshold

        # Calculate the turn rate.
        turn_rate = PROPORTIONAL_GAIN * deviation

        # Set the drive base speed and turn rate.
        robot.drive(DRIVE_SPEED, turn_rate)

        if (us.distance() < 100):
            stop_wait()

        if light.color() == Color.RED:
            break

        # command = s.recv(1024).decode("utf-8")
        # if command == "stop":
        #     break

    robot.stop()




s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
s.sendall(b"Commands please")

while 1:
    command = s.recv(1024).decode("utf-8")
    print(command)
    if command == "left":
        go_left()
    if command == "right":
        go_right()
    if command == "forward":
        go_forward()
    if command == "backward":
        go_backward()
    if command == "stop":
        stop()
    if command == "auto":
        auto_mode()
