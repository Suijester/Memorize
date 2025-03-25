from imports import *
from audio import recordAudio, transcribe
import os

def test_recording():
    filename = "test_memo.wav"
    
    print("Starting recording... Say 'end memo' to stop.")
    
    # Record audio
    recordAudio(filename)
    
    # Get the transcription
    transcript = transcribe(filename)
    
    # Print the transcription
    print("\nTranscription:")
    print(transcript["text"])
    
    return transcript

if __name__ == "__main__":
    test_recording()