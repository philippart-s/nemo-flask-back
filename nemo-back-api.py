from urllib import response
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

import soundfile as sf

# Transform the sound into a csv file.
# The sound is read from the global variable sended_sound
# Return: The builded dataset with the given sound
def build_dataframe():  
  # define the column names
  headers = 'filename length chroma_stft_mean chroma_stft_var rms_mean rms_var spectral_centroid_mean spectral_centroid_var spectral_bandwidth_mean \
      spectral_bandwidth_var rolloff_mean rolloff_var zero_crossing_rate_mean zero_crossing_rate_var harmony_mean harmony_var perceptr_mean perceptr_var tempo mfcc1_mean mfcc1_var mfcc2_mean \
      mfcc2_var mfcc3_mean mfcc3_var mfcc4_mean mfcc4_var\n'

  # calculate the value of the librosa parameters
  audio_time_series, sampling_rate_ori = sf.read(io.BytesIO(sended_sound))
  # Resampling to use the same samplingrate that the model use for training
  sampling_rate = 22050
  audio_time_series = librosa.resample(audio_time_series, sampling_rate_ori, sampling_rate)
  chroma_stft = librosa.feature.chroma_stft(y = audio_time_series, sr = sampling_rate)
  rmse = librosa.feature.rms(y = audio_time_series)
  spec_cent = librosa.feature.spectral_centroid(y = audio_time_series, sr = sampling_rate)
  spec_bw = librosa.feature.spectral_bandwidth(y = audio_time_series, sr = sampling_rate)
  rolloff = librosa.feature.spectral_rolloff(y = audio_time_series, sr = sampling_rate)
  zcr = librosa.feature.zero_crossing_rate(audio_time_series)
  mfcc = librosa.feature.mfcc(y = audio_time_series, sr = sampling_rate)
  to_append = f'uploaded-sound {np.mean(chroma_stft)} {np.mean(rmse)} {np.mean(spec_cent)} {np.mean(spec_bw)} {np.mean(rolloff)} {np.mean(zcr)}'
  for e in mfcc:
      to_append += f' {np.mean(e)}'
  
  # Return the dataset
  in_memory_csv = headers + to_append
  dataframe = pandas.read_csv(io.StringIO(in_memory_csv), sep=" ")

  return dataframe


# Try to predict the kind of marine mammal from the uploaded sound.
def predict():
  labels = "AtlanticSpottedDolphin\nBeardedSeal\nBeluga_WhiteWhale\nBlueWhale\nBottlenoseDolphin\nBoutu_AmazonRiverDolphin\nBowheadWhale\nClymeneDolphin\n\
Commerson'sDolphin\nCommonDolphin\nDall'sPorpoise\nDuskyDolphin\nFalseKillerWhale\nFin_FinbackWhale\nFinlessPorpoise\nFraser'sDolphin\nGrampus_Risso'sDolphin\n\
GraySeal\nGrayWhale\nHarborPorpoise\nHarbourSeal\nHarpSeal\nHeaviside'sDolphin\nHoodedSeal\nHumpbackWhale\nIrawaddyDolphin\nJuanFernandezFurSeal\nKillerWhale\n\
LeopardSeal\nLong_FinnedPilotWhale\nLongBeaked(Pacific)CommonDolphin\nMelonHeadedWhale\nMinkeWhale\nNarwhal\nNewZealandFurSeal\nNorthernRightWhale\n\
PantropicalSpottedDolphin\nRibbonSeal\nRingedSeal\nRossSeal\nRough_ToothedDolphin\nSeaOtter\nShort_Finned(Pacific)PilotWhale\nSouthernRightWhale\nSpermWhale"

  # Build the dataframe from the sound
  dataframe = build_dataframe()

  df_labels = pandas.read_csv(io.StringIO(labels), header=None)

  # encode the labels (0 => 44)
  converter = LabelEncoder()
  converter.fit_transform(df_labels.iloc[:,-1])
  
  # INPUTS: all other columns are inputs except the filename
  scaler = StandardScaler()
  # Pourquoi a-t-on besoin des datas ayant servi à faire l’entraînement ?
  df = pandas.read_csv('csv_files/data.csv')
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
def guess_mammal_marine_from_sound():

  request.args.get('sound_name')
  response = predict()

  return jsonify({'animal': response[0]})

## End-point to get the animal name from its sound
@app.route('/send-sound', methods=['POST'])
def upload_mammal_marine_sound():

  global sended_sound 
  sended_sound = request.get_data()

  return "ok"


## Main entry
if __name__ == '__main__':

  app.run(host='0.0.0.0', port=8080, debug=True)
