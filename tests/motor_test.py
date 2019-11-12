from adafruit_motorkit import MotorKit
from adafruit_motor import stepper

kit = MotorKit()

for x in range(100):
    kit.stepper1.onestep(direction=stepper.FORWARD, style=stepper.DOUBLE)
    kit.stepper1.release()

for x in range(100):
    kit.stepper1.onestep(direction=stepper.BACKWARD, style=stepper.DOUBLE)
    kit.stepper1.release()
