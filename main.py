from imports import *
import audioCommands
import wakeWord
import transcription
import os
import database

import warnings
warnings.filterwarnings("ignore", message = "FP16 is not supported on CPU; using FP32 instead")

def testRecording():
    print("Listening...")
    wakeWord.wakeHandler()
    print("Done.")

if __name__ == "__main__":
    testRecording()