#####################################################################################################################################################
###################################################################### IMPORTS ######################################################################
#####################################################################################################################################################
# ---------- Audio ----------
from audio.AudioProcessing import AudioProcessing as Audio
from audio.Speak import Speak 
# from audio.preRecordedDialogs.playHello import playHello
# from audio.preRecordedDialogs.playYouCanSpeak import playYouCanSpeak
# from audio.preRecordedDialogs.playDontKnow import playDontKnow

# ---------- Screen ----------
from screen.Screen import Screen
import pygame

# ---------- Servo ----------
from servo.Servo import Servo

# ---------- Others ----------
import time
import os

class Main:
    """
    This class is the main class wich manage all threads to interact with users. 
    """

    def __init__(self):
        "class constructor"
        self.running = True

        # Create a single screen thread that will run for the entire robot life
        self.screen = Screen(mode="speaking")
        self.screen.start()

    def start(self):
        """Manages events."""
        
        print("START robot")
        
        try:
            # -------- Introduction (hello/tuto) --------
            OUTPUT_PATH = os.path.join(os.path.dirname(__file__), ".", "audio", "preRecordedDialogs","hello.wav")
            audioHello = Speak(OUTPUT_PATH)
            servoR = Servo("rightArm")
            servoL = Servo("leftArm")

            # Start threads (screen already started in __init__)
            audioHello.start()
            servoR.start()
            servoL.start()

            while self.running:
                # Check that the response has finished being generated
                if not audioHello.is_alive():
                    print("Response generated, audio thread automatically stopped")
                    audioHello.stop()
                    servoR.stop()
                    servoL.stop()
                    self.running = False  # Exit loop
                time.sleep(0.1)  # Short pause to save CPU power


            # infinite loop, stop when robot switches off
            while True:
                self.running = True

                # -------- Audio acquisition and processing loop --------
                
                # class instances
                audio = Audio()
                OUTPUT_PATH = os.path.join(os.path.dirname(__file__), ".", "audio", "preRecordedDialogs","youCanSpeak.wav")
                audioYouCanSpeak = Speak(OUTPUT_PATH)

                # Change screen to speaking mode for introduction
                self.screen.change_mode("speaking")
                
                # Start threads
                audio.start()
                audioYouCanSpeak.start()
                audioYouCanSpeak.join()  # screen speaking mode until audioYouSpeak stops
                audioYouCanSpeak.stop()
                # Change to waiting mode for listening
                self.screen.change_mode("waiting")

                while self.running:

                    # Check that user stops speaking to change the display into "thinking" mode
                    if not audio.getUserSpeak(): 
                        self.screen.change_mode("thinking")

                    # Check that the response has finished being generated
                    if not audio.is_alive():
                        print("Response generated, audio thread stopped")
                        audio.stop()
                        self.running = False  # Exit loop

                    time.sleep(0.1)  # Short pause to save CPU power

                # -------- robot response loop --------
                self.running = True

                # Start robot response
                print("getAnswer=", audio.getAnswer())
                if audio.getAnswer() == None: # if wikipedia didn't find a response
                    print("la réponse est soit vide soit None")
                    # Change to teaching mode for responding
                    self.screen.change_mode("speaking")
                    # play dontKnow.wav file and turn head
                    OUTPUT_PATH = os.path.join(os.path.dirname(__file__), ".", "audio", "preRecordedDialogs","dontKnow.wav")
                    audioDontKnow = Speak(OUTPUT_PATH)
                    servoH = Servo("head")

                    servoH.start()
                    audioDontKnow.start()

                    while self.running:
                        # Check that the response has finished being saying
                        if not audioDontKnow.is_alive():
                            print("Robot finishes speaking")
                            servoH.stop()
                            audioDontKnow.stop()
                            self.running = False  # Exit loop

                        time.sleep(0.1)  # Short pause to save CPU power



                else: # if wikipedia found a response
                    # Change to teaching mode for responding
                    self.screen.change_mode("teaching")
                    OUTPUT_PATH = os.path.join(os.path.dirname(__file__), ".", "audio", "answer.wav") # !!!!! avec les .. ???
                    speak = Speak(OUTPUT_PATH)
                    speak.start()

                    while self.running:
                        # Checks that the robot has finished responding
                        if not speak.is_alive():
                            print("Robot finishes speaking: speaking thread automatically stopped")
                            speak.stop()
                            self.running = False  # Exit loop
                        time.sleep(0.1)  # Short pause to save CPU power
                    
        
        except Exception as e:
            print(f"Error in the main loop: {e}")
        # We don't stop the screen thread - it runs until program termination

if __name__ == "__main__":    
    robot = Main()
    robot.start()