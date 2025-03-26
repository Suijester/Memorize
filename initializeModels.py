from imports import *

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

whisper.load_model("small", device = "cpu");
whisper.load_model("base", device = "cpu");