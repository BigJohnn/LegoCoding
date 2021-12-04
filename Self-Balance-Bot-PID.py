# The Main logic is from networks, I just translate it into python. 
# This is a good start to learn PID.
# You can build the bot with your Lego 51515 or 45678. # In fact, or anything else. :D

from spike import PrimeHub, LightMatrix, Button, StatusLight, ForceSensor, MotionSensor, Speaker, ColorSensor, App, DistanceSensor, Motor, MotorPair
from spike.control import wait_for_seconds, wait_until, Timer
from math import *

hub = PrimeHub()

hub.light_matrix.show_image('HEART')
hub.speaker.beep()
hub.status_light.on('blue')
hub.light_matrix.off()

# Adjust this so that your bot is in some balance :D
target_pitch = 40

# 1. Set Ki and Kd to zero and gradually increase Kp so that the robot starts to oscillate about the zero position.

# 2. Increase Ki so that the response of the robot is faster when it is out of balance. Ki should be large enough so that the angle of inclination does not increase. The robot should come back to zero position if it is inclined.

# 3. Increase Kd so as to reduce the oscillations. The overshoots should also be reduced by now.

# 4. Repeat the above steps by fine tuning each parameter to achieve the best result.

Kp = 14.5
Ki = 108
Kd = 15

print('Kp=',Kp)
print('Ki=',Ki)
print('Kd=',Kd)

motor = MotorPair('A','B')
motor.set_default_speed(100)
Integral = 0

distance_sensor = DistanceSensor('D')
distance_sensor.light_up(100,100,0,0)

error_prev = 0
timer = Timer()
timer.reset()
motor.start()
while True:

    error = target_pitch - hub.motion_sensor.get_pitch_angle()
    
    if error < 5:
        distance_sensor.light_up_all(50)
    else:
        distance_sensor.light_up_all(0)

    Integral = Integral + error * timer.now()

    timer.reset()
    
    if error_prev == 0:
        error_prev = error
    
    derivative = error - error_prev
    error_prev = error
    
    result = error * Kp + Integral * Ki + derivative * Kd
    
    motor.start_at_power(floor(result))
    
motor.stop()
