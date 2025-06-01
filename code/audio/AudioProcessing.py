#####################################################################################################################################################
###################################################################### IMPORTS #######################################################################
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

class AudioProcessing(threading.Thread):
    """
    This class acquires an audio signal from the raspberry's USB 1 port with sounddevice while the 
    user holds down the pushbutton on GPIO PORT 4. 
    The signal is then converted into a text query for wikipedia thanks to vosk. 
    A text summary of the wikipedia page is then generated, which in turn is converted into an 
    audio file thanks to piper.
    """

    def __init__ (self):
        """
            This function is the constructor of the class.
            In:
                * self:   Reference to the current object.
            Out:
                * A new instance of the class.
        """
        # ---------- initialise parallelism ----------
        super().__init__()
        self._running = True
        self._lock = threading.Lock()
        self.userSpeak = True # True if user is speaking or robot waiting for the question 

        # ---------- Configuration Speech to text ----------
        self.BUTTON_PIN = 4
        self.AUDIO_CHANNEL = 1
        self.INPUT_FILENAME = os.path.join(os.path.dirname(__file__), "..", "audio", "recorded.wav")
        self.MODEL_PATH_STT = os.path.join(os.path.dirname(__file__), "..", "lib", "vosk-model-small-fr-0.22")
        self.q = queue.Queue() #queue of recorded data

        # ---------- Configuration Wikipedia ----------
        wikipedia.set_lang("fr")
        self.answer = None

        # ---------- Configuration Text to speech ----------
        self.MODEL_PATH_TTS = os.path.join(os.path.dirname(__file__), "..", "lib", "fr_FR-siwis-medium.onnx")
        self.PIPER_PATH = os.path.join(os.path.dirname(__file__), "..", "lib", "piper","piper")
        self.OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "..", "audio", "answer.wav")

#############################################################################################################################
#################################################### Thread methods #########################################################
#############################################################################################################################

    def run(self):
        """Main method executed in the thread."""
        
        try:
            self.recordingAudio()
            self.userSpeak = False
            query = self.stt()
            if query == "": #wikipedia doesn't support empty query
                self.answer = None 
            else:
                self.wikipedia(query)
                if self.answer != None: # wikipedia response can be None if it doesn't find the answer
                    self.tts(self.answer)
        
        except Exception as e:
            print(f"Error in AudioProcessing thread: {e}")

    def stop(self):
        """Stop generating answer """
        self._running = False

#############################################################################################################################
#################################################### Speech to text #########################################################
#############################################################################################################################
    
    def callback(self,indata, frames:int, time, status):
        """
            Function called for each new data block during audio recording
            In:
                * self : Reference to the current object.
                * indata : NumPy array containing the audio captured in the current block
                * frames : Number of audio samples
                * time : Object containing timestamps
                * status : Indicates if any error occurred, such as buffer underflow/overflow
        """
        if status:
            print(status)
        self.q.put(indata.copy())

    def recordingAudio(self):
        """
            This function acquires an audio signal from the raspberry's USB port with sounddevice 
            while the user holds down the pushbutton on GPIO PORT. 
            It then write a .wav file with the recorded data.
            In:
                * self: Reference to the current object.

            Out:
                *  result : the text corresponding to the recorded audio
        """

        try:
            # ---------- Configurations ----------
            SAMPLE_RATE = 16000

            # ---------- GPIO Setup ----------
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

            # ---------- Audio recording button pressed ---------
            while GPIO.input(self.BUTTON_PIN) == GPIO.HIGH:
                pass  # button not pressed

            recorded_frames = []

            with sd.InputStream(samplerate=SAMPLE_RATE, channels=self.AUDIO_CHANNEL, callback=self.callback):
                while GPIO.input(self.BUTTON_PIN) == GPIO.LOW:
                    recorded_frames.append(self.q.get())

            # ---------- Save as WAV ----------
            recorded_data = np.concatenate(recorded_frames, axis=0)
            with wave.open(self.INPUT_FILENAME, 'wb') as wf:
                wf.setnchannels(self.AUDIO_CHANNEL)
                wf.setsampwidth(2)  # 16 bits
                wf.setframerate(SAMPLE_RATE)
                wf.writeframes((recorded_data * 32767).astype(np.int16).tobytes())

        except Exception as e:
            print(f"Error in recordingAudio method: {e}")


    def stt(self):
        """
            This function converts the recorded audio file into text with vosk and sends it back.
            In:
                * self: Reference to the current object.

            Out:
                *  result : the text corresponding to the recorded audio
        """
        try:
            # ---------- Configurations ----------
            SAMPLE_RATE = 16000

            # ---------- Transcribe with vosk ----------
            model = Model(self.MODEL_PATH_STT)
            recognizer = KaldiRecognizer(model, SAMPLE_RATE)

            with wave.open(self.INPUT_FILENAME, "rb") as wf:
                while True:
                    data = wf.readframes(4000)
                    if len(data) == 0:
                        break
                    recognizer.AcceptWaveform(data)

            result = json.loads(recognizer.FinalResult())
            print(result.get("text", ""))
            return result.get("text", "")

        except Exception as e:
            print(f"Error in stt method: {e}")

#############################################################################################################################
#################################################### Wikipedia ##############################################################
#############################################################################################################################
    def wikipedia(self, query:str):
        """
            This function generates a summary in 1 sentence of the wikipedia 
            page corresponding to the query
            In:
                * self : Reference to the current object.
                * query : the text query for wikipedia
            Out:
                * A summary of the wikipedia page
        """
        import warnings
        from bs4 import GuessedAtParserWarning
        warnings.filterwarnings("ignore", category=GuessedAtParserWarning)

        try:
            self.answer = wikipedia.summary(query, sentences=1)

        except Exception as e:
            print(f"Error in wikipedia method: {e}")
            self.answer = None
    
    def getAnswer(self):
        return self.answer


#############################################################################################################################
#################################################### Text to speech #########################################################
#############################################################################################################################
    def tts(self, text:str):
        """
            This function generates an audio file of the robot's answer.
            In:
                * self : Reference to the current object.
                * text : the text answer
            Out:
                * A summary of the wikipedia page
        """
        # Define the command to call Piper
        piper_command = [
            self.PIPER_PATH, "--model", self.MODEL_PATH_TTS,"--output_file", self.OUTPUT_PATH]

        # Call Piper via subprocess
        subprocess.run(
        piper_command,
        input=text.encode('utf-8'),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)

#############################################################################################################################
#################################################### Play answer #########################################################
#############################################################################################################################
    def getAnswerPath(self):
        return self.OUTPUT_PATH
    
    def getUserSpeak(self):
        return self.userSpeak


    def play(self, audio_path):

        # Play the audio file
        pygame.mixer.init()
        pygame.mixer.music.load(audio_path) 
        pygame.mixer.music.play()
        # Wait for the audio to finish playing
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)

