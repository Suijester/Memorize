from imports import *

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

whisper.load_model("base", device = "cpu");
model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')