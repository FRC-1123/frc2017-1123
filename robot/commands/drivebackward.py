import logging

import wpilib
from wpilib.command import Command

import subsystems
from rectifieddrive import RectifiedDrive


# FIXME: Distance calculation does not seem to work correctly!
class DriveBackward(Command):
    """
    Drives backward the given distance in inches.
    """

    def __init__(self, dist):
        super().__init__('Driving forward %d inches' % dist)

        self.requires(subsystems.motors)

        self.drive = RectifiedDrive(0, 0.05)
        self.timer = wpilib.Timer()

        self.desired_dist = dist * 1024 / 18.85  # convert from inches to edges
        self.last_position = None
        self.dist_traveled = 0  # in edges

        self.logger = logging.getLogger("robot")

    def initialize(self):
        self.last_position = subsystems.motors.left_motor.getPosition()
        self.timer.start()

    def execute(self):
        self.drive.rectified_drive(-0.3, 0)
        self.timer.delay(0.05)

    def isFinished(self):
        # timeout after 10 seconds
        if self.timeSinceInitialized() > 3:
            return True

        position = subsystems.motors.left_motor.getPosition()
        self.logger.info("Encoder position:  {}".format(position))
        if position > self.last_position:
            self.dist_traveled += self.last_position + 1024 - position
        else:
            self.dist_traveled += self.last_position - position
        if self.dist_traveled >= self.desired_dist:
            return True

        self.last_position = position
        return False

    def end(self):
        # set outputs to 0 on end
        subsystems.motors.robot_drive.setLeftRightMotorOutputs(0, 0)
