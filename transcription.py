from imports import *

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

import warnings
warnings.filterwarnings("ignore", message = "FP16 is not supported on CPU; using FP32 instead")
transcriber = whisper.load_model("small", device = "cpu");
smallTranscriber = whisper.load_model("small", device = "cpu");

def transcribe(filename):
    transcription = transcriber.transcribe(filename, language = "en", temperature = 0)
    return transcription

def wakeTranscribe():
    transcription = smallTranscriber.transcribe("listening.wav", language = "en", temperature = 0)
    return transcription