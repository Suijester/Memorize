from imports import *
from recordAudio import recordAudio
from wakeWord import wakeWord
import transcription
import os

import warnings
warnings.filterwarnings("ignore", message = "FP16 is not supported on CPU; using FP32 instead")

def testRecording():
    filename = "test_memo.wav"
    wakeWord()
    
    print("Starting recording... Say 'end memo' to stop.")
    recordAudio(filename)
    transcript = transcription.transcribe(filename)
    
    print("\nTranscription:")
    print(transcript["text"])
    
    return transcript

if __name__ == "__main__":
    testRecording()