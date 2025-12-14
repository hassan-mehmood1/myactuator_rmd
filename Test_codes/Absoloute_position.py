# -*- coding: gbk -*-
import myactuator_rmd_py as rmd
import time
driver = rmd.CanDriver("can0")
actuator = rmd.ActuatorInterface(driver, 1)

# Move to 180 degree position at 100 deg/s
actuator.sendPositionAbsoluteSetpoint(180.0, 300.0)
time.sleep(5)  # Wait for motor to reach target position

# Get current position
angle = actuator.getMultiTurnAngle()
print(f"Current position: {angle}°")

time.sleep(5)
mode = actuator.getControlMode()
print(f"Current control mode: {mode}")
actuator.shutdownMotor()