# -*- coding: gbk -*-
import myactuator_rmd_py as rmd
import time
import os
os.system("sudo ip link set can0 down")
time.sleep(1)
os.system("sudo ip link set can0 up type can bitrate 1000000")
time.sleep(1)

driver = rmd.CanDriver("can0")
# actuator = rmd.ActuatorInterface(driver, 1)
# actuator.setCurrentPositionAsEncoderZero()
print("Current position set as encoder zero point")

# actuator.shutdownMotor()
# time.sleep(1)  # Wait for shutdown
actuator = rmd.ActuatorInterface(driver, 1)  # Reinitialize actuator interface
angle = actuator.getMultiTurnAngle()
print(f"Current position: {angle}°")

actuator.shutdownMotor()
time.sleep(1)  # Wait for shutdown

os.system("sudo ip link set can0 down")