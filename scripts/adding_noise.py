from xml.dom.minicompat import NodeList
import pydub
from pydub import AudioSegment
import os 
import shutil 
import uuid

# paths to the data audio files 
backgrounds_path = os.path.join(os.getcwd() , 'backgrounds') 
records_path = os.path.join(os.getcwd() , 'data' , 'recorded-data') 

# looping through the noise audio files 
for noise_file in os.listdir(backgrounds_path) : 
    noise_path = os.path.join(backgrounds_path , noise_file)
    for dir in ['positive' , 'negative'] : 
        # looping through the recorded audio files 
        for record in os.listdir(os.path.join(records_path , dir)) : 
            record_path = os.path.join(records_path , dir , record)
            destination_path = os.path.join(records_path , dir)
            noise = AudioSegment.from_wav(noise_path) 
            # take the first 3 seconds from the noise file 
            noise = noise[:3000] 
            clean_record = AudioSegment.from_wav(record_path ) 
            # adding noise 
            noise_record = noise.overlay(clean_record) 
            noise_record.export(os.path.join(destination_path , f'{str(uuid.uuid1())}.wav' ) , format='wav')


            