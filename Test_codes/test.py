import myactuator_rmd_py as rmd
import time
import os
os.system("sudo ip link set can0 down")
time.sleep(1)
os.system("sudo ip link set can0 up type can bitrate 1000000")
time.sleep(1)

# Initialize CAN driver and actuator interface
time.sleep(2)
driver = rmd.CanDriver("can0")  # Using can0
actuator = rmd.ActuatorInterface(driver, 1)  # CAN ID set to 1
actuator.setCurrentPositionAsEncoderZero()
time.sleep(2)
# actuator.shutdownMotor()
# time.sleep(1)  # Wait for shutdown
# actuator = rmd.ActuatorInterface(driver, 1)  # Reinitialize actuator interface

angle = actuator.getMultiTurnAngle()
print(f"Current position: {angle}°")
time.sleep(1)
actuator.sendPositionAbsoluteSetpoint(180.0, 30.0)
time.sleep(8)
angle = actuator.getMultiTurnAngle()
print(f"Current position: {angle}°")
actuator.shutdownMotor()
time.sleep(1)  # Wait for shutdown
# Get version number
# print("Version number:", actuator.getVersionDate())
os.system("sudo ip link set can0 down")