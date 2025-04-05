from imports import *
import audioCommands
from wakeWord import wakeWord
import transcription
import os
import database

import warnings
warnings.filterwarnings("ignore", message = "FP16 is not supported on CPU; using FP32 instead")

def testRecording():
    print("Listening...")
    wakeWord()
    
    print("Starting recording... Say 'end memo' to stop.")
    audioCommands.recordAudio()

    print("\nAll memos in database:")
    database.printAllMemos()
    
    print("\nDeleting all memos:")
    database.deleteAllMemos()

    print("Done.")

if __name__ == "__main__":
    testRecording()