from imports import *
import transcription
import database

def recordAudio(filename = datetime.now().strftime("%m-%d-%Y-%H-%M-%S") + ".wav", sampler = 16000):
    beep()
    tempFilename = "tempAudio.wav"

    wf = wave.open(filename, "wb")
    wf.setnchannels(1)
    wf.setsampwidth(4)
    wf.setframerate(sampler)

    # deque so buffer is easier to manipulate
    audioBuffer = deque(maxlen = int((sampler * 5) / 1024) + 1)
    framesInBuffer = 0 # number of frames currently in the buffer
    framesPerCheck = 20; # number of frames that needs to occur for us to check if end memo is said
    frameCount = 0 # number of frames TOTAl since start of processing
    
    silentFrames = 0
    silenceThreshold = 6    

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
                    with wave.open(tempFilename, "wb") as tempwf:
                        tempwf.setnchannels(1)
                        tempwf.setsampwidth(4)
                        tempwf.setframerate(sampler)
                        recentAudio = np.concatenate(recentFrames, axis = 0)
                        tempwf.writeframes(recentAudio.tobytes())

                    abridge = transcription.transcribe(tempFilename)
                    transcribedText = abridge["text"].lower()
                    print(transcribedText);

                    # if user stops talking for a while, we can just end the memo
                    if not transcribedText.strip():
                        silentFrames += 1
                        if silentFrames > silenceThreshold:
                            beep()
                            break
                    else:
                        silentFrames = 0

                    # use fuzzy so we can see if words similar to "end memo" were said
                    fuzzyThreshold = 80
                    if (fuzz.partial_ratio("end memo", transcribedText) >= fuzzyThreshold):
                        beep()
                        break

    finally:
        stream.stop()
        wf.close()
        abridge = transcription.transcribe(filename)
        transcribedText = abridge["text"]
        print("Transcribed text: " + transcribedText)
        print()
        database.saveMemo(filename, transcribedText)
        if os.path.exists(tempFilename):
            os.remove(tempFilename)


def queryAudio(sampler = 16000):
    beep()

    tempFilename = "tempQuery.wav"
    filename = "query.wav"
    
    wf = wave.open(filename, "wb")
    wf.setnchannels(1)
    wf.setsampwidth(4)
    wf.setframerate(sampler)

    audioBuffer = deque(maxlen = int((sampler * 5) / 1024) + 1)
    framesInBuffer = 0
    framesPerCheck = 20
    frameCount = 0
    
    silentFrames = 0
    silenceThreshold = 5
    
    try:
        with sounddevice.InputStream(samplerate = sampler, channels = 1, dtype = np.int32, blocksize = 4096) as stream:
            while True:
                frame, _ = stream.read(1024)
                wf.writeframes(frame.tobytes())
                
                audioBuffer.append(frame)
                framesInBuffer += frame.shape[0]
                
                if len(audioBuffer) == audioBuffer.maxlen:
                    framesInBuffer -= audioBuffer[0].shape[0]
                
                frameCount += 1
                if frameCount % framesPerCheck == 0:
                    framesChecked = min(30, len(audioBuffer))
                    recentFrames = list(audioBuffer)[-framesChecked:]
                    
                    with wave.open(tempFilename, "wb") as tempwf:
                        tempwf.setnchannels(1)
                        tempwf.setsampwidth(4)
                        tempwf.setframerate(sampler)
                        recentAudio = np.concatenate(recentFrames, axis = 0)
                        tempwf.writeframes(recentAudio.tobytes())

                    abridge = transcription.transcribe(tempFilename)
                    query = abridge["text"].lower()

                    if not query.strip():
                        silentFrames += 1
                        if silentFrames > silenceThreshold:
                            beep()
                            break
                    else:
                        silentFrames = 0

                    fuzzyThreshold = 80
                    if (fuzz.partial_ratio("end query", query) >= fuzzyThreshold):
                        beep()
                        break

    finally:
        stream.stop()
        wf.close()
        abridge = transcription.transcribe(filename)
        query = abridge["text"]
        print("Query:" + query)
        print()
        database.queryMemos(query)
        if os.path.exists(tempFilename):
            os.remove(tempFilename)


def deleteAudio(sampler = 16000):
    beep()

    tempFilename = "tempDelete.wav"
    filename = "delete.wav"
    
    wf = wave.open(filename, "wb")
    wf.setnchannels(1)
    wf.setsampwidth(4)
    wf.setframerate(sampler)

    audioBuffer = deque(maxlen = int((sampler * 5) / 1024) + 1)
    framesInBuffer = 0
    framesPerCheck = 20
    frameCount = 0

    silentFrames = 0
    silenceThreshold = 5
    
    try:
        with sounddevice.InputStream(samplerate = sampler, channels = 1, dtype = np.int32, blocksize = 4096) as stream:
            while True:
                frame, _ = stream.read(1024)
                wf.writeframes(frame.tobytes())
                
                audioBuffer.append(frame)
                framesInBuffer += frame.shape[0]
                
                if len(audioBuffer) == audioBuffer.maxlen:
                    framesInBuffer -= audioBuffer[0].shape[0]
                
                frameCount += 1
                if frameCount % framesPerCheck == 0:
                    framesChecked = min(30, len(audioBuffer))
                    recentFrames = list(audioBuffer)[-framesChecked:]
                    
                    with wave.open(tempFilename, "wb") as tempwf:
                        tempwf.setnchannels(1)
                        tempwf.setsampwidth(4)
                        tempwf.setframerate(sampler)
                        recentAudio = np.concatenate(recentFrames, axis = 0)
                        tempwf.writeframes(recentAudio.tobytes())

                    abridge = transcription.transcribe(tempFilename)
                    deleteQuery = abridge["text"].lower()

                    if not deleteQuery.strip():
                        silentFrames += 1
                        if silentFrames > silenceThreshold:
                            beep()
                            break
                    else:
                        silentFrames = 0

                    fuzzyThreshold = 80
                    if (fuzz.partial_ratio("end deletion", deleteQuery) >= fuzzyThreshold):
                        beep()
                        break

    finally:
        stream.stop()
        wf.close()
        abridge = transcription.transcribe(filename)
        deletionQuery = abridge["text"]
        database.deleteMemobyQuery(deletionQuery)
        if os.path.exists(tempFilename):
            os.remove(tempFilename)


    
def beep():
    try:
        sampleRate = 44100
        duration = 0.3
        frequency = 1000

        t = np.linspace(0, duration, int(sampleRate * duration), False)
        beep_data = 0.5 * np.sin(2 * np.pi * frequency * t)
        
        beep_data = (beep_data * 32767).astype(np.int16)
        
        sounddevice.play(beep_data, sampleRate)
        sounddevice.wait()
        
    except Exception as e:
        print(f"Beep sound failed. Recording anyway.")
