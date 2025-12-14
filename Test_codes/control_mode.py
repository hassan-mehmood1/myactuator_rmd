# -*- coding: gbk -*-
import myactuator_rmd_py as rmd
import time
driver = rmd.CanDriver("can0")
actuator = rmd.ActuatorInterface(driver, 1)
mode = actuator.getControlMode()
print(f"Current Control Mode: {mode}")