from imports import *
from recordAudio import recordAudio
import transcription
import os

import warnings
warnings.filterwarnings("ignore", message = "FP16 is not supported on CPU; using FP32 instead")

def test_recording():
    filename = "test_memo.wav"
    
    print("Starting recording... Say 'end memo' to stop.")
    
    # Record audio
    recordAudio(filename)
    
    # Get the transcription
    transcript = transcription.transcribe(filename)
    
    # Print the transcription
    print("\nTranscription:")
    print(transcript["text"])
    
    return transcript

if __name__ == "__main__":
    test_recording()