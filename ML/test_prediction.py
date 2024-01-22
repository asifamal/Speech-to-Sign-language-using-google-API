##importing modules
import numpy as np
import pandas as pd
import librosa
import tensorflow as tf
from tensorflow.keras.models import load_model
import speech_recognition as sr


def predict():

	
	model=load_model("ML/model.h5")

	##
	NUM_MFCC = 13
	N_FFT = 2048
	HOP_LENGTH = 512
	SAMPLE_RATE = 22050
	DOWN_SAMPLE_RATE = 16000

	data = {"features": []}

	def extract_features(data, sample_rate):
		mfcc = librosa.feature.mfcc(data, sample_rate, n_mfcc=NUM_MFCC, n_fft=N_FFT, hop_length=HOP_LENGTH)
		feature = mfcc.T
		return feature
		
	def noise(data):
		noise_amp = 0.5*np.random.uniform()*np.amax(data)
		data = data + noise_amp*np.random.normal(size=data.shape[0])
		return data
		
	def stretch(data, rate=0.8):
		return librosa.effects.time_stretch(data, rate)
		
	def pitch(data, sampling_rate, pitch_factor=0.7):
		return librosa.effects.pitch_shift(data, sampling_rate, pitch_factor)
		
		
	signal, sample_rate = librosa.load("media/input/test.wav", sr=SAMPLE_RATE)
		
	# Cropping & Resampling
	start_time = 0.4  # Start time in seconds
	end_time = 1.9  # End time in seconds
	start_frame = int(start_time * sample_rate)
	end_frame = int(end_time * sample_rate)
	signal = signal[start_frame:end_frame]
	signal = librosa.resample(signal, sample_rate, DOWN_SAMPLE_RATE)
		
	# Add noise
	signal = noise(signal)
	#res1 = extract_features(signal, DOWN_SAMPLE_RATE)
	#data["features"].append(np.array(res1))
		
	# Stretch and shift pitch
	new_data = stretch(signal)[:24000]
	data_stretch_pitch = pitch(new_data, DOWN_SAMPLE_RATE)
	res2 = extract_features(data_stretch_pitch, DOWN_SAMPLE_RATE)
	data["features"].append(np.array(res2))


	Features = pd.DataFrame()
	Features['features'] = data["features"]


	X = np.asarray(Features['features'])

	# Pad Features to make them of equal length
	X = tf.keras.preprocessing.sequence.pad_sequences(X)

	#print(X.shape)
	#print(X)
	labels = ['neutral', 'happy', 'surprise', 'unpleasant']
	y_pred = model.predict(X)
	y_pred = np.argmax(y_pred, axis=1)#labels = {'neutral':0, 'happy':1, 'surprise':2, 'unpleasant': 3}


	#print("Result:",labels[y_pred[0]])
	return labels[y_pred[0]]
	
#result=predict()
#print("Result:",result)
	