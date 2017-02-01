import logging

import wpilib
from networktables import NetworkTables
from wpilib.command import Command
from robotpy_ext.common_drivers.navx import AHRS


import subsystems
from commands.setspeed import SetSpeed

logging.basicConfig(level=logging.DEBUG)


class UpdateNetworkTables(Command):
    '''
    This command will read the joystick's y axis and use that value to control
    the speed of the SingleMotor subsystem.
    '''

    def __init__(self):
        super().__init__('Update NetworkTables')

        self.navx = AHRS.create_spi()

        self.logger = logging.getLogger("robot")

        self.sd = NetworkTables.getTable("SmartDashboard")
        self.nt_timer = wpilib.Timer()  # timer for updating NetworkTables
        self.nt_timer.start()

    def execute(self):
        if self.nt_timer.hasPeriodPassed(.2):  # update NetworkTables every 0.2 seconds
            # dashboard forward button (for demonstration purposes)
            if self.sd.containsKey("forwardCommand") and self.sd.getBoolean("forwardCommand"):  # check if move forward button pressed
                self.sd.putBoolean("forwardCommand", False)
                SetSpeed(0.5, 1).start()  # move forward at half power for one second
                self.logger.info("Moving forward at half power for one second.")


            # update navX status
            self.sd.putBoolean('navX/isConnected', self.navx.isConnected())
            self.sd.putBoolean('navX/isCalibrating', self.navx.isCalibrating())
            # self.sd.putNumber('navX/angle', self.navx.getAngle())
            self.sd.putNumber('navX/yaw', self.navx.getYaw())

            # update motor output statuses
            self.sd.putNumber("leftOutput", subsystems.motors.left_motor.getSetpoint())
            self.sd.putNumber("rightOutput", subsystems.motors.right_motor.getSetpoint())
