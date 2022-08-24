from torch_model import model 
import torch 
import torchaudio
import torchaudio.functional as F
import uuid 
import os 
import pyaudio
import wave 
import numpy as np 
import pyttsx3


# load the model 
model = model()
model.load_state_dict(torch.load(os.path.join(os.getcwd() , 'torch.pth')))
model.eval()

chunk = 1024  # Record in chunks of 1024 sampl
sample_format = pyaudio.paInt16  # 16 bits per sample
channels = 1
fs = 44100  # Record at 44100 samples per second
seconds = 3

try : 
    while True :  
        print('start record ')
        p = pyaudio.PyAudio()  # Create an interface to PortAudio
        stream = p.open(format=sample_format,
                                channels=channels,
                                rate=fs,
                                frames_per_buffer=chunk,
                                input=True)
        frames = []  
        # Store data in chunks for 3 seconds
        for _ in range(0, int(fs / chunk * seconds)):
                    data = stream.read(chunk)
                    frames.append(data)

        # Stop and close the stream 
        stream.stop_stream()
        stream.close()
        # Terminate the PortAudio interface
        p.terminate()
        
        # save the frames as wav file 
        wf = wave.open('output.wav', 'wb')
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(sample_format))
        wf.setframerate(fs)
        wf.writeframes(b''.join(frames))
        wf.close()

        def load_and_preprocess(filename):
            # load the file 
            wav, sample_rate = torchaudio.load(filename )
            # pick the first channel 
            wav = wav[0 , :]
            # resample 
            wav = F.resample(wav, sample_rate, 16000) 
            padding = 48000 - wav.shape[0] 
            zeros = torch.zeros([padding]) 
            wav = torch.cat([zeros , wav] , axis = 0 )
            # spectrogram 
            transform = torchaudio.transforms.Spectrogram(n_fft=320 )
            spectrogram = transform(wav)
            spectrogram = spectrogram.unsqueeze(0)
            return spectrogram 



        spectrogram = load_and_preprocess('output.wav')
        spectrogram = spectrogram.unsqueeze(0)

        # predict 
        with torch.no_grad() : 
            pred = model(spectrogram)

        pred = [1 if pred > .8  else 0]

        # if the prediction is true we get response 
        if pred[0] == 1 : 
            engine = pyttsx3.init()
            voice = engine.getProperty('voices') #get the available voices
            engine.setProperty('voice', voice[0].id) #changing voice to index 1 for female voice
            engine.say("hello" )
            engine.runAndWait()

except KeyboardInterrupt :  
    os.remove('output.wav')



   

    


    