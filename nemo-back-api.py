import librosa


# transform the sound into a csv file
def transform_wav_to_csv(sound_saved):  
  # define the column names
  headers = 'filename length chroma_stft_mean chroma_stft_var rms_mean rms_var spectral_centroid_mean spectral_centroid_var spectral_bandwidth_mean \
      spectral_bandwidth_var rolloff_mean rolloff_var zero_crossing_rate_mean zero_crossing_rate_var harmony_mean harmony_var perceptr_mean perceptr_var tempo mfcc1_mean mfcc1_var mfcc2_mean \
      mfcc2_var mfcc3_mean mfcc3_var mfcc4_mean mfcc4_var'.split()
  
  # create the csv file
  file = open(f'csv_files/{os.path.splitext(sound_saved)[0]}.csv', 'w', newline = '')
  with file:
      writer = csv.writer(file)
      writer.writerow(header_test)
      
  # calculate the value of the librosa parameters
  sound_name = f'audio_files/{sound_saved}'
  y, sr = librosa.load(sound_name, mono = True, duration = 30)
  chroma_stft = librosa.feature.chroma_stft(y = y, sr = sr)
  rmse = librosa.feature.rms(y = y)
  spec_cent = librosa.feature.spectral_centroid(y = y, sr = sr)
  spec_bw = librosa.feature.spectral_bandwidth(y = y, sr = sr)
  rolloff = librosa.feature.spectral_rolloff(y = y, sr = sr)
  zcr = librosa.feature.zero_crossing_rate(y)
  mfcc = librosa.feature.mfcc(y = y, sr = sr)
  to_append = f'{os.path.basename(sound_name)} {np.mean(chroma_stft)} {np.mean(rmse)} {np.mean(spec_cent)} {np.mean(spec_bw)} {np.mean(rolloff)} {np.mean(zcr)}'
  for e in mfcc:
      to_append += f' {np.mean(e)}'
  
  # fill in the csv file
  file = open(f'csv_files/{os.path.splitext(sound_saved)[0]}.csv', 'a', newline = '')
  with file:
      writer = csv.writer(file)
      writer.writerow(to_append.split())
  
  # create test dataframe
  df_test = pd.read_csv(f'csv_files/{os.path.splitext(sound_saved)[0]}.csv')
  
  # each time you add a sound, a line is added to the test.csv file
  # if you want to display the whole dataframe, you can deselect the following line
  #st.write(df_test)
  
  return df_test

#transform_wav_to_csv('test.wav')
