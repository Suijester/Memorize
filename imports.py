import whisper
import sounddevice
import numpy as np
import wave
import sqlite3
import pyttsx3
import re
from transformers import pipeline
import pvporcupine, pvrecorder, simpleaudio as audio
import os
from datetime import datetime
from collections import deque
from fuzzywuzzy import fuzz