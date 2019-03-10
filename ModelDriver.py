from keras.models import load_model
from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img
import pandas as pd
import numpy as np
import sys
import PIL
import cv2

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

batch_size = 1
img_width = 48
img_height = 48

emotions = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']

def load_process_image(fileloc):
	img = cv2.imread(fileloc)
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	faces = face_cascade.detectMultiScale(gray, 1.3, 5)
	for (x,y,w,h) in faces:
		print(x,y,w,h)
		cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
		crop_gray = gray[y:y+h, x:x+w]
		resized_gray = cv2.resize(crop_gray, (48,48))
	return resized_gray


# Usage: python predict.py classifiers/classifier_batch200_augmented_val_acc_0.5305.h5 data/fer2013_private_test.csv tmp
# (0=Angry, 1=Disgust, 2=Fear, 3=Happy, 4=Sad, 5=Surprise, 6=Neutral)

def get_emotion(predictions):
	emotion = emotions[np.argmax(predictions)]
	return emotion

def make_prediction(r_image, modelloc):
	model = load_model(modelloc)
	model.summary()  #Verifying model structure
	#load image
	image = np.expand_dims(r_image, axis=2)[np.newaxis,:]
	predictions = model.predict(image, 1 )
	emotion = get_emotion(predictions)
	print(predictions)
	print(emotion)

def do_all(fileloc):
	r_image = load_process_image(fileloc)
	emotion = make_prediction(r_image, "classifier_b.h5")
	print(emotion)
