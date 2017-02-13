import logging

from wpilib.command import PIDCommand

import robot
import subsystems
from commands.followjoystick import FollowJoystick
from inputs import camera
from inputs import oi

logging.basicConfig(level=logging.INFO)


class DriveToRod(PIDCommand):
    """
    This command will find the rod and drive the robot towards it.
    """

    def __init__(self):
        # PID constants
        kp = 0.01
        ki = 0.005
        kd = 0.002
        kf = 0.0
        ktolerance = 0.02

        # initialize PID controller with a period of 0.05 seconds
        super().__init__(kp, ki, kd, 0.05, kf, "Drive To Rod")

        self.requires(subsystems.motors)

        turnController = self.getPIDController()
        turnController.setInputRange(-1.0, 1.0)
        turnController.setOutputRange(-1.0, 1.0)
        turnController.setAbsoluteTolerance(ktolerance)
        turnController.setContinuous(True)

        self.logger = logging.getLogger("robot")

        self.is_lost = False  # can't find the rod

        self.last_output = 0  # for if the rod is lost

    def returnPIDInput(self):
        if oi.controller.getStartButton():  # return control back to controller
            FollowJoystick().start()
            return 0
        rod_pos = camera.get_rod_pos()
        if rod_pos is None:
            self.logger.critical("Couldn't find the rod!")
            self.is_lost = True
            if not robot.is_autonomous:  # return control to controller if not in autonomous
                self.logger.critical("Returned control to the controller!")
                FollowJoystick().start()
            return 0
        else:
            error = .5 - rod_pos[0]  # error as horizontal distance from center
            self.logger.info("current rod error: {}".format(error))
            return error

    def usePIDOutput(self, output):
        if self.is_lost:  # if lost, slowly spin in circle
            # TODO: check signs of motor outputs
            if self.last_output > 0:  # keep turning right
                subsystems.motors.robot_drive.setLeftRightMotorOutputs(0.1, 0.1)
            else:  # keep turning left
                subsystems.motors.robot_drive.setLeftRightMotorOutputs(-0.1, -0.1)
        else:
            subsystems.motors.robot_drive.drive(.4, output)
            self.last_output = output
