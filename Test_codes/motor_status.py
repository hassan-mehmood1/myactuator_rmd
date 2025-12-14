# -*- coding: gbk -*-
import myactuator_rmd_py as rmd
import time
driver = rmd.CanDriver("can0")
actuator = rmd.ActuatorInterface(driver, 1)

# Motor Status 1
status1 = actuator.getMotorStatus1()
print(f"""
Motor Status 1:
Temperature: {status1.temperature}C
Brake Status: {'Released' if status1.is_brake_released else 'Locked'}
Voltage: {status1.voltage}V
Error Code: {status1.error_code}
""")

# Motor Status 2
status2 = actuator.getMotorStatus2()
print(f"""
Motor Status 2:
Temperature: {status2.temperature}C
Current: {status2.current}A
Shaft Speed: {status2.shaft_speed} RPM
Shaft Angle: {status2.shaft_angle}Degree
""")

# Motor Status 3
status3 = actuator.getMotorStatus3()
print(f"""
Motor Status 3:
Temperature: {status3.temperature}°C
Phase A Current: {status3.current_phase_a}A
Phase B Current: {status3.current_phase_b}A
Phase C Current: {status3.current_phase_c}A
""")
