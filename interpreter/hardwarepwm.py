from rpi_hardware_pwm import HardwarePWM
from time import sleep

pwm = HardwarePWM(pwm_channel=1, hz=50)
pwm.start(100) # full duty cycle
SLEEP_TIME = .03
MAX = 180


pwm.change_duty_cycle(50)

def percent_to_duty(angle):
    # return 
    duty = 3+ angle/180*8

    print(angle,":",duty)
    return float(duty)

for i in range(0,180):

    pwm.change_duty_cycle(percent_to_duty(i))
    sleep(SLEEP_TIME)

for i in range(MAX,0,-1):
    pwm.change_duty_cycle(percent_to_duty(i))
    sleep(SLEEP_TIME)

# pwm.change_frequency(25_000)

pwm.stop()
