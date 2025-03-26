from imports import *

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

transcriber = whisper.load_model("small", device = "cpu");