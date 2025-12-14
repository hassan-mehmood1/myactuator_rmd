# -*- coding: gbk -*-
import myactuator_rmd_py as rmd
import time

driver = rmd.CanDriver("can0")
actuator = rmd.ActuatorInterface(driver, 1)

speed = 300.0      # deg/s
wait_time = 2    # seconds
actuator.sendPositionAbsoluteSetpoint(0.0, 300)
time.sleep(wait_time)
angle = actuator.getMultiTurnAngle()
print(f"Position: {angle:.2f}°")
try:
    # while True:
    # Move to 10 degrees
    start_time = time.perf_counter()
    print("loop start")
    while(angle<99):
        actuator.sendPositionAbsoluteSetpoint(100.0, speed)
        # time.sleep(wait_time)
        angle = actuator.getMultiTurnAngle()
    elapsed = time.perf_counter() - start_time
    print(f"Position: {angle:.2f}°, Time: {elapsed:.3f} s")

        # Move back to 0 degrees
        # start_time = time.perf_counter()
        # actuator.sendPositionAbsoluteSetpoint(0.0, speed)
        # time.sleep(wait_time)
        # angle = actuator.getMultiTurnAngle()
        # elapsed = time.perf_counter() - start_time
        # print(f"Target: 0°, Position: {angle:.2f}°, Time: {elapsed:.3f} s")

except KeyboardInterrupt:
    print("Stopping motor...")

finally:
    mode = actuator.getControlMode()
    print(f"Final control mode: {mode}")
    actuator.shutdownMotor()
