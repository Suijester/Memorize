summarizer = pipeline("summarizer", model = "t5-small")
transcriber = whisper.load_model("base")

def recordAudio(filename, sampler = 16000):
    beep()
    
    wf = wave.open(filename, "wb")
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(sampler)

    audioBuffer = []
    bufferLength = 5
    capSamples = bufferLength * sampler

    completeAudio = []
    # quick math, bufferLength * 16000 = 80000 here, 80000/1024 ~= 77 rounded down, so audioBuffer can hold max of 77 frames, but almost always will hold less
    try:
        with sounddevice.InputStream(samplerate = sampler, channels = 1, dtype = np.int16) as stream:
            while True:
                frame, _ = stream.read(1024)
                completeAudio.append(frame)
                wf.writeframes(frame.tobytes())
                audioBuffer.append(frame)

                bufferSamples = sum(f.shape[0] for f in audioBuffer)
                while bufferSamples > capSamples and len(audioBuffer) > 1:
                    audioBuffer.pop(0)
                    bufferSamples = sum(f.shape[0] for f in audioBuffer)

                if len(audioBuffer) % 20 == 0 and len(audioBuffer) > 0:
                    framesChecked = min(30, len(audioBuffer))
                    recentFrames = audioBuffer[-framesChecked:]
                    with wave.open("temp_audio_memo.wav", "wb") as tempwf:
                        tempwf.setnchannels(1)
                        tempwf.setsampwidth(2)
                        tempwf.setframerate(sampler)
                        recentAudio = np.concatenate(recentFrames, axis = 0)
                        tempwf.writeframes(recentAudio.tobytes())
                    
                    abridge = transcriber.transcribe("temp.wav")
                    if "end memo" in abridge["text"].lower():
                        beep()
                        break


    finally:
        stream.stop()
        wf.close()
        if os.path.exists("temp_audio_memo.wav"):
            os.remove("temp_audio_memo.wav")

        transcript = transcriber.transcribe(filename)
        transcriptName = filename[:-4] + ".txt"


# note to self, go get that beep.wav file
def beep():
    audio.WaveObject.from_wave_file("beep.wav").play()