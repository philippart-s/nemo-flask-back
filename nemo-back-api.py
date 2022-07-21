from flask import Flask, request, jsonify
import flask

import os
import librosa
import numpy as np
import pandas
import csv

import io

from keras.models import load_model
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import LabelEncoder


# transform the sound into a csv file
# Parameters:
#  - sound_saved : the binary file saved for a sound
# Return: The builded dataset with the given sound
def build_dataset(sound_saved: str):  
  # define the column names
  headers = 'filename length chroma_stft_mean chroma_stft_var rms_mean rms_var spectral_centroid_mean spectral_centroid_var spectral_bandwidth_mean \
      spectral_bandwidth_var rolloff_mean rolloff_var zero_crossing_rate_mean zero_crossing_rate_var harmony_mean harmony_var perceptr_mean perceptr_var tempo mfcc1_mean mfcc1_var mfcc2_mean \
      mfcc2_var mfcc3_mean mfcc3_var mfcc4_mean mfcc4_var'.split()
  
  # create the csv file
  file = open(f'csv_files/{os.path.splitext(sound_saved)[0]}.csv', 'w', newline = '')
  with file:
      writer = csv.writer(file)
      writer.writerow(headers)
      
  # calculate the value of the librosa parameters
  sound_name = f'audio_files/{sound_saved}'
  audio_time_series, sampling_rate = librosa.load(sound_name, mono = True, duration = 30)
  chroma_stft = librosa.feature.chroma_stft(y = audio_time_series, sr = sampling_rate)
  rmse = librosa.feature.rms(y = audio_time_series)
  spec_cent = librosa.feature.spectral_centroid(y = audio_time_series, sr = sampling_rate)
  spec_bw = librosa.feature.spectral_bandwidth(y = audio_time_series, sr = sampling_rate)
  rolloff = librosa.feature.spectral_rolloff(y = audio_time_series, sr = sampling_rate)
  zcr = librosa.feature.zero_crossing_rate(audio_time_series)
  mfcc = librosa.feature.mfcc(y = audio_time_series, sr = sampling_rate)
  to_append = f'{os.path.basename(sound_name)} {np.mean(chroma_stft)} {np.mean(rmse)} {np.mean(spec_cent)} {np.mean(spec_bw)} {np.mean(rolloff)} {np.mean(zcr)}'
  for e in mfcc:
      to_append += f' {np.mean(e)}'
  
  # fill in the csv file
  file = open(f'csv_files/{os.path.splitext(sound_saved)[0]}.csv', 'a', newline = '')
  with file:
      writer = csv.writer(file)
      writer.writerow(to_append.split())
  
  # Return the dataset
  dataset = pandas.read_csv(f'csv_files/{os.path.splitext(sound_saved)[0]}.csv')
  
  return dataset


# Classify the uploded sounds trensformed in a CSV format compatible.
def classification(sound_name: str):
  # Label to display the founded marine mammal
  """ labels = "AtlanticSpottedDolphin\nBeardedSeal\nBeluga_WhiteWhale\nBlueWhale\nBottlenoseDolphin\nBoutu_AmazonRiverDolphin\nBowheadWhale\nClymeneDolphin\n\
Commerson'sDolphin\nCommonDolphin\nDall'sPorpoise\nDuskyDolphin\nFalseKillerWhale\nFin_FinbackWhale\nFinlessPorpoise\nFraser'sDolphin\nGrampus_Risso'sDolphin\n\
GraySeal\nGrayWhale\nHarborPorpoise\nHarbourSeal\nHarpSeal\nHeaviside'sDolphin\nHoodedSeal\nHumpbackWhale\nIrawaddyDolphin\nJuanFernandezFurSeal\nKillerWhale\n\
LeopardSeal\nLong_FinnedPilotWhale\nLongBeaked(Pacific)CommonDolphin\nMelonHeadedWhale\nMinkeWhale\nNarwhal\nNewZealandFurSeal\nNorthernRightWhale\n\
PantropicalSpottedDolphin\nRibbonSeal\nRingedSeal\nRossSeal\nRough_ToothedDolphin\nSeaOtter\nShort_Finned(Pacific)PilotWhale\nSouthernRightWhale\nSpermWhale" """

  dataframe = build_dataset(sound_name)

  #df_test = pandas.read_csv(io.StringIO(labels), sep=",", header=None)

  df = pandas.read_csv('csv_files/data.csv')

  # encode the labels (0 => 44)
  converter = LabelEncoder()
  converter.fit_transform(df.iloc[:,-1])
  
  # INPUTS: all other columns are inputs except the filename
  scaler = StandardScaler()
  # Pourquoi a-t-on besoin des datas ayant servi à faire l’entraînement ?
  scaler.fit(np.array(df.iloc[:, 1:27]))
  x = scaler.transform(np.array(dataframe.iloc[:, 1:27]))

  # load the pretrained model
  model = load_model('saved_model/my_model')
  
  # generate predictions for test samples
  predictions = model.predict(x)
  
  # generate argmax for predictions
  classes = np.argmax(predictions, axis = 1)
  
  # transform class number into class name
  result = converter.inverse_transform(classes)

  return result


app = Flask(__name__)
## End-point to get the animal name from its sound
@app.route('/get-animal-name', methods=['GET'])
def GetMarineMammal():

  sound_name = request.args.get('sound_name')
  print(sound_name)
  response = classification(sound_name + ".wav")

  return jsonify({'animal': response[0]})

## End-point to get the animal name from its sound
@app.route('/send-sound', methods=['POST'])
def UploadSound():

  with open(os.path.join('audio_files/', 'sound-uploaded.wav'),'wb') as f:
         f.write(request.get_data())

  return jsonify({'file-name': 'sound-uploaded.wav'})


## Main entry
if __name__ == '__main__':

  app.run(host='0.0.0.0', port=8080, debug=True)
