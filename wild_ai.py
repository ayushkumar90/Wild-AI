# -*- coding: utf-8 -*-
"""Wild_AI.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Ud8DP1nfhHjnPjLX9Ki5tZ6jxybBF5GC
"""

#mount google drive
from google.colab import drive
drive.mount('/content/drive')

path_root = r'/content/drive/MyDrive/ProbeSet'

import sys
import os
from math import log
import numpy as np
import scipy as sp
from PIL import Image
import matplotlib.pyplot as plt

from keras.preprocessing.image import ImageDataGenerator
batches = ImageDataGenerator().flow_from_directory(directory=path_root, target_size=(64,64), batch_size=10000)

batches.class_indices

!pip install pillow

imgs, labels = next(batches)

imgs.shape

labels.shape

def plots(ims, figsize=(20,30), rows=10, interp=False, titles=None):
    if type(ims[0]) is np.ndarray:
        ims = np.array(ims).astype(np.uint8)
        if (ims.shape[-1] != 3):
            ims = ims.transpose((0,2,3,1))
    f = plt.figure(figsize=figsize)
    cols = 10 
    for i in range(0,50):
        sp = f.add_subplot(rows, cols, i+1)
        sp.axis('Off')
        if titles is not None:
            sp.set_title(list(batches.class_indices.keys())[np.argmax(titles[i])], fontsize=16)
        plt.imshow(ims[i], interpolation=None if interp else 'none')

plots(imgs, titles = labels)

classes = batches.class_indices.keys()
classes

perc = (sum(labels)/labels.shape[0])*100

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(imgs/255.,labels, test_size=0.3,random_state=1)

X_train.shape

X_test.shape

y_train.shape

y_test.shape

from tensorflow.keras.layers import BatchNormalization

import keras
from keras.models import Sequential, Input, Model
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
#from keras.layers.normalization import BatchNormalization

num_classes = 2

import tensorflow as tf

def Wild_AI():
    Wild_AI = Sequential()
    Wild_AI.add(Conv2D(16, kernel_size=(3, 3),
                     activation='relu',
                     input_shape=(64,64,3)))
    Wild_AI.add(MaxPooling2D(pool_size=(2, 2)))
    Wild_AI.add(Conv2D(32, (3, 3), activation='relu'))
    Wild_AI.add(MaxPooling2D(pool_size=(2, 2)))
    Wild_AI.add(Conv2D(64, (3, 3), activation='relu'))
    Wild_AI.add(MaxPooling2D(pool_size=(2, 2)))
    Wild_AI.add(Dropout(0.25))
    Wild_AI.add(Flatten())
    Wild_AI.add(Dense(128, activation='relu'))
    Wild_AI.add(Dense(2,kernel_regularizer=tf.keras.regularizers.l2(0.01), activation='softmax'))
    Wild_AI.compile(optimizer = 'rmsprop', loss = 'binary_crossentropy', metrics=['accuracy'])
    return Wild_AI

from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint

Wild_AI = Wild_AI()

early_stop = EarlyStopping(monitor='val_accuracy', 
                               mode='max', 
                               patience = 5 ,
                               restore_best_weights=True)


mc = ModelCheckpoint('WildAI.h5', monitor='val_accuracy', mode='max', verbose=1, save_best_only=True)
mode=Wild_AI.fit(X_train, y_train, validation_data=(X_test, y_test),
                epochs = 100, 
                verbose = 2,
                batch_size = 64,
                callbacks = [early_stop,mc]
            )

y_train.shape

y_train_new = np.argmax(y_train, axis=1)

y_train_new

scores = Wild_AI.evaluate(X_test, y_test)

scores = Wild_AI.evaluate(X_train, y_train)

print('CNN accuracy: ', scores[1])

print('CNN loss: ', scores[0])

import pandas as pd

y_p=Wild_AI.predict(X_test) 
y_pred=np.argmax(y_p,axis=1)

y_test2 = np.argmax(y_test, axis=1)

from sklearn import metrics
c_matrix = metrics.confusion_matrix(y_test2, y_pred)

print(c_matrix)