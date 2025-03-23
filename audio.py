summarizer = pipeline("summarizer", model = "t5-small")
transcriber = whisper.load_model("base")

def recordAudio(filename, sampler = 16000):
    beep()

    wf = wave.open(filename, "wb")
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(sampler)

    # deque so buffer is easier to manipulate
    audioBuffer = deque(maxlen = int((sampler * 5) / 1024) + 1)
    framesInBuffer = 0 # number of frames currently in the buffer
    framesPerCheck = 20; # number of frames that needs to occur for us to check if end memo is said
    frame_count = 0 # number of frames TOTAl since start of processing
    
    try:
        with sounddevice.InputStream(samplerate = sampler, channels = 1, dtype = np.int16) as stream:
            while True:
                frame, _ = stream.read(1024)
                wf.writeframes(frame.tobytes())
                
                # add a frame to buffer, increment framesInBuffer by the size of the frame
                audioBuffer.append(frame)
                framesInBuffer += frame.shape[0]
                
                # if we hit maxlen, we have to remove frames from both audioBuffer (which does it automatically), and decrement framesInBuffer
                if len(audioBuffer) == audioBuffer.maxlen:
                    framesInBuffer -= audioBuffer[0].shape[0]
                
                frame_count += 1
                if frame_count % framesPerCheck == 0:
                    # check for the end words, 'end memo'
                    framesChecked = min(30, len(audioBuffer))
                    recentFrames = list(audioBuffer)[-framesChecked:]
                    
                    # open a wav file that we can stuff all the recent audio frames into and check for 'end memo'
                    temp_filename = "temp_audio_memo.wav"
                    with wave.open(temp_filename, "wb") as tempwf:
                        tempwf.setnchannels(1)
                        tempwf.setsampwidth(2)
                        tempwf.setframerate(sampler)
                        recentAudio = np.concatenate(recentFrames, axis = 0)
                        tempwf.writeframes(recentAudio.tobytes())

                    abridge = transcriber.transcribe(temp_filename)
                    transcribed_text = abridge["text"].lower()
                    
                    # use fuzzy so we can see if words similar to "end memo" were said
                    fuzzyThreshold = 80
                    if (fuzz.partial_ratio("end memo", transcribed_text) >= fuzzyThreshold):
                        beep()
                        break

    finally:
        stream.stop()
        wf.close()
        temp_filename = "temp_audio_memo.wav"
        if os.path.exists(temp_filename):
            os.remove(temp_filename)

        summary = summarize(filename)
        transcript = transcribe(filename)
        date = datetime.now().strftime("%Y-%m-%d")
        # reminder to finish transcribing
        saveToDatabase(filename, summary, transcript, date)

# note to self, go get that beep.wav file
def beep():
    audio.WaveObject.from_wave_file("beep.wav").play()
