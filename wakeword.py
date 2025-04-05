from imports import *
import audioCommands
import transcription

def wakeWord(sampler = 16000):

    audioBuffer = deque(maxlen = int((sampler * 4) / 1024) + 1)
    framesInBuffer = 0 # number of frames currently in the buffer
    framesPerCheck = 20; # number of frames that needs to occur for us to check if end memo is said
    frameCount = 0 # number of frames TOTAl since start of processing

    try:
        with sounddevice.InputStream(samplerate = sampler, channels = 1, dtype = np.int32, blocksize = 4096) as stream:
            while True:
                frame, _ = stream.read(1024)
                
                # add a frame to buffer, increment framesInBuffer by the size of the frame
                audioBuffer.append(frame)
                framesInBuffer += frame.shape[0]
                
                # if we hit maxlen, we have to remove frames from both audioBuffer (which does it automatically), and decrement framesInBuffer
                if len(audioBuffer) == audioBuffer.maxlen:
                    framesInBuffer -= audioBuffer[0].shape[0]
                
                frameCount += 1
                if frameCount % framesPerCheck == 0:
                    framesChecked = min(30, len(audioBuffer))
                    recentFrames = list(audioBuffer)[-framesChecked:]
                    
                    # open a wav file that we can stuff all the recent audio frames into and check for the wake word
                    with wave.open("listening.wav", "wb") as tempwf:
                        tempwf.setnchannels(1)
                        tempwf.setsampwidth(4)
                        tempwf.setframerate(sampler)
                        recentAudio = np.concatenate(recentFrames, axis = 0)
                        tempwf.writeframes(recentAudio.tobytes())

                    abridge = transcription.wakeTranscribe()
                    transcribedText = abridge["text"].lower();

                    fuzzyThreshold = 80
                    if (fuzz.partial_ratio("start memo", transcribedText) >= fuzzyThreshold or fuzz.partial_ratio("start recording", transcribedText) >= fuzzyThreshold):
                        print("Wake word detected!")
                        return "record"
                        break

                    if (fuzz.partial_ratio("delete memo", transcribedText) >= fuzzyThreshold or fuzz.partial_ratio("delete recording", transcribedText) >= fuzzyThreshold):
                        print("Delete word detected!")
                        return "delete"
                        break

                    if (fuzz.partial_ratio("query", transcribedText) >= fuzzyThreshold or fuzz.partial_ratio("question", transcribedText) >= fuzzyThreshold):
                        print("Query detected!")
                        return "query"
                        break

    finally:
        stream.stop()
        if os.path.exists("listening.wav"):
            os.remove("listening.wav")


def wakeHandler():
    try:
        command = wakeWord()
        if command == "record":
            audioCommands.recordAudio()
        elif command == "delete":
            audioCommands.deleteAudio()
        elif command == "query":
            audioCommands.queryAudio()
    except Exception as e:
        print(f"Error with Wake Word: {e}")