#####################################################################################################################################################
###################################################################### IMPORTS ######################################################################
#####################################################################################################################################################

import RPi.GPIO as GPIO
import sounddevice as sd
import numpy as np
import queue
import wave
import os
import json
import wikipedia
import pygame
import time
import subprocess
import threading
from vosk import Model, KaldiRecognizer

class Speak(threading.Thread):
    """
    This class makes the robot talk by reading a .wav file
    """

    def __init__ (self, OUTPUT_PATH):
        """
            This function is the constructor of the class.
            In:
                * self:   Reference to the current object.
                * OUTPUT_PATH: the path to the .wav file to be read
            Out:
                * A new instance of the class.
        """
        # ---------- initialise parallelism ----------
        super().__init__()
        self._running = True
        self._lock = threading.Lock()

        # ---------- Configuration Text to speech ----------
        self.OUTPUT_PATH = OUTPUT_PATH

#############################################################################################################################
#################################################### Thread methods #########################################################
#############################################################################################################################

    def run(self):
        """Main method executed in the thread."""
        
        try:
            self.playAudio(self.OUTPUT_PATH)
        
        except Exception as e:
            print(f"Error in Speak thread: {e}")

    def stop(self):
        """Stop speaking """
        self._running = False

#############################################################################################################################
#################################################### Text to speech #########################################################
#############################################################################################################################
    def playAudio(self, audioPath):
        """
            This function read a .wav file.
            In:
                * self : Reference to the current object.
                * audioPath : the path of .wav file
            Out:
                * A summary of the wikipedia page
        """

        # Play the audio file
        pygame.mixer.init()
        pygame.mixer.music.load(audioPath) 
        pygame.mixer.music.play()
        # Wait for the audio to finish playing
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)
