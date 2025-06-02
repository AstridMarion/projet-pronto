#####################################################################################################################################################
###################################################################### IMPORTS ######################################################################
#####################################################################################################################################################
import RPi.GPIO as GPIO
import time
from adafruit_servokit import ServoKit
import threading

class Servo(threading.Thread):
    """
    This class rotates the robot's right arm by + or - 180°.
    """

    def __init__ (self, servoName):
        """
            This function is the constructor of the class.
            In:
                * self:   Reference to the current object.
                * servoName: must be "rightArm", "leftArm" or "head"
            Out:
                * A new instance of the class.
        """
        # initialise parallelism
        super().__init__()
        self._running = False
        self._lock = threading.Lock()

        # define kit and set GPIO for OE port
        self.servoName = servoName
        self.kit = ServoKit(channels=16)
        self.OE_PIN = 17  # GPIO 17 (PIN 11)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.OE_PIN, GPIO.OUT)

        GPIO.output(self.OE_PIN, GPIO.HIGH) # inactive servos
    
#############################################################################################################################
#################################################### Thread methods #########################################################
#############################################################################################################################

    def run(self):
        """Main method executed in the thread."""

        self._running = True
        
        try:
            self.move()
        
        except Exception as e:
            print(f"Error in servo thread: {e}")
    
    def stop(self):
        """Stop servo thread """
        self._running = False

#############################################################################################################################
#################################################### Move servo #########################################################
#############################################################################################################################
    def move(self):
        """ 
        This function turns the servos 180° in one direction then the other if it's the arms, 
        and 90° then -180° then 90° if it's the head
        """
        GPIO.output(self.OE_PIN, GPIO.LOW) # active servos

        if self.servoName == "rightArm":
            servoPin = 2

            #stop head servo
            self.kit.continuous_servo[1].throttle = 0

            self.kit.continuous_servo[servoPin].throttle = 0.4
            time.sleep(0.6)
            self.kit.continuous_servo[servoPin].throttle = -0.4
            time.sleep(0.5)

            #stop right arm servo
            self.kit.continuous_servo[servoPin].throttle = 0
           
            GPIO.output(self.OE_PIN, GPIO.HIGH)
            
        elif self.servoName == "leftArm":
            servoPin = 0
            #stop head servo
            self.kit.continuous_servo[1].throttle = 0

            self.kit.continuous_servo[servoPin].throttle = -0.4
            time.sleep(0.6)
            self.kit.continuous_servo[servoPin].throttle = 0.4
            time.sleep(0.5)

            #stop right arm servo
            self.kit.continuous_servo[servoPin].throttle = 0

            GPIO.output(self.OE_PIN, GPIO.HIGH)
        
        elif self.servoName == "head":
            servoPin = 1
            #stop other servos
            self.kit.continuous_servo[0].throttle = 0
            self.kit.continuous_servo[2].throttle = 0

            self.kit.continuous_servo[servoPin].throttle = -0.2
            time.sleep(0.2)
            self.kit.continuous_servo[servoPin].throttle = 0.2
            time.sleep(0.4)
            self.kit.continuous_servo[servoPin].throttle = -0.2
            time.sleep(0.2)

            #stop head servo
            self.kit.continuous_servo[servoPin].throttle = 0
            GPIO.output(self.OE_PIN, GPIO.HIGH)

        else:
            print(self.servoName + "invalid")

