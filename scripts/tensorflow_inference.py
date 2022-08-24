import uuid 
import os 
import pyaudio
import wave
import tensorflow as tf 
import numpy as np 
import tensorflow_io as tfio
import pyttsx3


# load the model 
model = tf.keras.models.load_model(os.path.join(os.getcwd() ,'trigger_word_0'))


chunk = 1024  # Record in chunks of 1024 sampl
sample_format = pyaudio.paInt16  # 16 bits per sample
channels = 2
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

        def load_wav_16k_mono(filename):
            # Load encoded wav file
            file_contents = tf.io.read_file(filename)
            # Decode wav (tensors by channels) 
            wav, sample_rate = tf.audio.decode_wav(file_contents, desired_channels=1)
            # Removes trailing axis
            wav = tf.squeeze(wav, axis=-1)
            sample_rate = tf.cast(sample_rate, dtype=tf.int64)
            # Goes from 44100Hz to 16000hz - amplitude of the audio signal
            wav = tfio.audio.resample(wav, rate_in=sample_rate, rate_out=16000)
            return wav 

        def preprocess(file_path): 
            wav = load_wav_16k_mono(file_path)
            # adding zeros to make it in suitable length 
            zero_padding = tf.zeros([48000] - tf.shape(wav), dtype=tf.float32)
            wav = tf.concat([zero_padding, wav],0)
            spectrogram = tf.signal.stft(wav, frame_length=320, frame_step=32)
            spectrogram = tf.abs(spectrogram)
            spectrogram = tf.expand_dims(spectrogram, axis=2)
            return spectrogram

        spectrogram = preprocess('output.wav')
        spectrogram = tf.expand_dims(spectrogram , 0 )

        # predict 
        pred = model.predict(spectrogram)
        pred = [1 if pred > .8  else 0]

        # if the prediction is true we get response 
        if pred[0] == 1 : 
            engine = pyttsx3.init()
            voice = engine.getProperty('voices') #get the available voices
            engine.setProperty('voice', voice[1].id) #changing voice to index 1 for female voice
            engine.say("hello" )
            engine.runAndWait()

except KeyboardInterrupt : 
    os.remove('output.wav')
    
    



    
