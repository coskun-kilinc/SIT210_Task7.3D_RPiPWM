import RPi.GPIO as GPIO
import time
LED = 11
TRIGGER = 13
ECHO = 15

# setup GPIO mode and pinouts
GPIO.setmode(GPIO.BOARD)
GPIO.setup(LED, GPIO.OUT)
GPIO.setup(TRIGGER, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

# boring way - GPIO pwm control
pwm = GPIO.PWM(LED, 100)
pwm.start(0)

def distance():
    # output HIGH on trigger
    GPIO.output(TRIGGER, HIGH)
    # sleep for 10 microseconds
    time.sleep(10/1000000)
    # stop output on trigger
    GPIO.output(TRIGGER, LOW)
    # start time is set to when signal was sent
    # while GPIO.input(ECHO) == LOW:
    start = time.time_ns()
    # end time is set once signal is received on echo
    while GPIO.input(ECHO) == HIGH:
        end = time.time_ns()
    # duration = time echo was received - time it was sent
    duration = end - start
    # distance = duration * speed of sound / 2 (duration * speed of sound is the time to the object and back, we only want the time from the object back)
    distance = (duration*0.034/2)
    return distance

try:
    while True:
        # get distance value
        dist = distance()
        print("Distance {distance:1.2f}")
        # duty cycle is set to 100 (max value) - distance, rounded to 1 decimal placev
        duty_cycle = round(100 - distance, 1)
        if duty_cycle < 0:
            duty_cycle = 0.0
        pwm.ChangeDutyCycle(duty_cycle)
        time.sleep(0.01)
        
    

except KeyboardInterrupt:
    pass
pwm.stop()
GPIO.cleanup()
