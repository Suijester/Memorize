from imports import *
import transcription

def recordAudio(filename, sampler = 16000):
    beep()

    wf = wave.open(filename, "wb")
    wf.setnchannels(1)
    wf.setsampwidth(4)
    wf.setframerate(sampler)

    # deque so buffer is easier to manipulate
    audioBuffer = deque(maxlen = int((sampler * 5) / 1024) + 1)
    framesInBuffer = 0 # number of frames currently in the buffer
    framesPerCheck = 20; # number of frames that needs to occur for us to check if end memo is said
    frameCount = 0 # number of frames TOTAl since start of processing
    
    try:
        with sounddevice.InputStream(samplerate = sampler, channels = 1, dtype = np.int32, blocksize = 4096) as stream:
            while True:
                frame, _ = stream.read(1024)
                wf.writeframes(frame.tobytes())
                
                # add a frame to buffer, increment framesInBuffer by the size of the frame
                audioBuffer.append(frame)
                framesInBuffer += frame.shape[0]
                
                # if we hit maxlen, we have to remove frames from both audioBuffer (which does it automatically), and decrement framesInBuffer
                if len(audioBuffer) == audioBuffer.maxlen:
                    framesInBuffer -= audioBuffer[0].shape[0]
                
                frameCount += 1
                if frameCount % framesPerCheck == 0:
                    # check for the end words, 'end memo'
                    framesChecked = min(30, len(audioBuffer))
                    recentFrames = list(audioBuffer)[-framesChecked:]
                    
                    # open a wav file that we can stuff all the recent audio frames into and check for 'end memo'
                    temp_filename = "temp_audio_memo.wav"
                    with wave.open(temp_filename, "wb") as tempwf:
                        tempwf.setnchannels(1)
                        tempwf.setsampwidth(4)
                        tempwf.setframerate(sampler)
                        recentAudio = np.concatenate(recentFrames, axis = 0)
                        tempwf.writeframes(recentAudio.tobytes())

                    abridge = transcription.transcribe(temp_filename)
                    transcribedText = abridge["text"].lower();
                    print(transcribedText);
                    # use fuzzy so we can see if words similar to "end memo" were said
                    fuzzyThreshold = 80
                    if (fuzz.partial_ratio("end memo", transcribedText) >= fuzzyThreshold):
                        beep()
                        break

    finally:
        stream.stop()
        wf.close()
        temp_filename = "temp_audio_memo.wav"
        if os.path.exists(temp_filename):
            os.remove(temp_filename)

# Generate and play a beep sound programmatically
def beep():
    try:
        # Generate a simple beep using numpy
        sample_rate = 44100  # standard audio sample rate
        duration = 0.3  # seconds
        frequency = 1000  # Hz
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        beep_data = 0.5 * np.sin(2 * np.pi * frequency * t)
        
        # Convert to int16 for sounddevice
        beep_data = (beep_data * 32767).astype(np.int16)
        
        # Play the beep
        sounddevice.play(beep_data, sample_rate)
        sounddevice.wait()  # Wait until the sound finishes playing
        
    except Exception as e:
        print(f"Beep sound failed. Recording anyway.")
