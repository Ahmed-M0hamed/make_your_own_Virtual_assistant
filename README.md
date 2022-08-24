# make your own siri 

this is a trigger word detection project made with python and tensorflow and pytorch so the project can 
be divided into phases so let me walk you through it 

## create dataset 
so we need two categories of audio clips [positive , negative ] or ones  have the trigger word and ones are not 
so the first python script we wrote is recording 20 clips for each category and gave them unique ids 
and save them as wav files  

---------------------

positive clips : just record the word you want to use it as trigger word 
----------------------
negative clips : record any kind of words or just let the record empty and it better to do both 

## adding noise 
so we need to add some kind of background noise to the records to make the model learn better and do some 
kind of data augemention  

## train the model 
you need to make a data pipeline to process the data after that you create the model and train it 

## inference 
finially you want to make live prediction 

## how to run the app 

- clone the repo 
```bash 
git clone the repo 
pip install -t requirments.txt 
``` 

- create the dataset 
```bash 
python scripts/recording.py 
``` 
- adding noise 
```bash
python scripts/adding_noise.py
``` 
- the model 
tensorflow => 
open the tensorflow_trigger_word.ipynb notebook and run all cells to train the model and save it 

----------------

pytorch => 
open the pytorch_trigger_word.ipynb notebook and run all cells to train the model and save it 


- do inference 
if your followed tensorflow notebook 
```bash 
python scripts/tensorflow_inference.py 
``` 
----------------

if you followed pytorch notebook
```bash 
python scripts/pytorch_inference.py 
``` 
