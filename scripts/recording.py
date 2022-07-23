from scipy.io.wavfile import  write 
import sounddevice as sd
import uuid 
import os 


fs = 44100
duration = 3 

# loop through both positive an negative dirs 
for dir in ['positive' , 'negative'] : 
    # 20 itieration for each dir 
    for i in range(20 ): 
        print(f'start record {i}')
        # record the audio 
        record = sd.rec(int(fs * duration) , samplerate = fs , channels = 2 )
        sd.wait()
        # initiate unique id 
        id = uuid.uuid1()
        path = os.path.join(os.getcwd() , 'data' ,dir , str(id))
        # save the record as wav file 
        write(f'{path}.wav' , fs , record)
        print(f'record {i} complete')

