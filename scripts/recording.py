import uuid 
import os 
import pyaudio
import wave

chunk = 1024  # Record in chunks of 1024 sampl
sample_format = pyaudio.paInt16  # 16 bits per sample
channels = 1 # it could be 1 or 2 
fs = 44100  # Record at 44100 samples per second
seconds = 3

for dir in ['positive' , 'negative'] : 
    if not os.path.exists(os.path.join(os.getcwd() , 'data' , 'recorded-data' , dir)) : 
        os.makedirs(os.path.join(os.getcwd() , 'data' , 'recorded-data' , dir))
    for i in range(20) : 
        file_path = os.path.join(os.getcwd() , 'data' , 'recorded-data' , dir , f'{str(uuid.uuid1())}.wav' )
        p = pyaudio.PyAudio()  # Create an interface to PortAudio
        print(f'start {dir} record :{i+1}')
        stream = p.open(format=sample_format,
                        channels=channels,
                        rate=fs,
                        frames_per_buffer=chunk,
                        input=True)

        frames = []  # Initialize array to store frames

        # Store data in chunks for 3 seconds
        for _ in range(0, int(fs / chunk * seconds)):
            data = stream.read(chunk)
            frames.append(data)

        # Stop and close the stream 
        stream.stop_stream()
        stream.close()
        # Terminate the PortAudio interface
        p.terminate()

        print(f'Finished {dir} record {i +1}')

        # Save the recorded data as a WAV file
        wf = wave.open(file_path, 'wb')
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(sample_format))
        wf.setframerate(fs)
        wf.writeframes(b''.join(frames))
        wf.close()