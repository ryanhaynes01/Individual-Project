import matplotlib.pyplot as plt
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Dense, Flatten
import tensorflow as tf
import file_handler
import numpy as np
import cv2
import os

fm = file_handler.FileManager()

labels = ['monster_original']
images_path = fm.create_path_string('application', 'frame_ouput', 'monster_original')

# avoid out of memory errors
#gpus = tf.config.experimental.list_physical_devices('GPU')
#for gpu in gpus:
#    tf.config.experimental.get_memory_growth(gpu, True)

train_data = tf.keras.utils.image_dataset_from_directory(fm.create_path_string('application', 'bin', 'training'))
validation_data = tf.keras.utils.image_dataset_from_directory(fm.create_path_string('application', 'bin', 'testing'))

train_data.map(lambda x, y: (x / 255, y))

#data_interator = train_data

train_data_iterator = train_data.as_numpy_iterator()
batch = train_data_iterator.next()

model = Sequential()

model.add(Conv2D(16, (3, 3), 1, activation='relu', input_shape=(256, 256, 3)))
model.add(MaxPooling2D())

model.add(Conv2D(32, (3, 3), 1, activation='relu'))
model.add(MaxPooling2D())

model.add(Conv2D(16, (3, 3), 1, activation='relu'))
model.add(MaxPooling2D())

model.add(Flatten())
model.add(Dense(256, activation='relu'))
model.add(Dense(1, activation='sigmoid'))

model.compile('adam', loss=tf.losses.BinaryCrossentropy(), metrics=['accuracy'])

tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir='log')

hist = model.fit(train_data, epochs=20, validation_data=validation_data, callbacks=[tensorboard_callback])


fig, ax = plt.subplots(ncols=4, figsize=(20, 20))
for idx, img in enumerate(batch[0][:4]):
    ax[idx].imshow(img.astype(int))
    ax[idx].title.set_text(batch[1][idx])

plt.show()


class_names = train_data.class_names
#img = cv2.imread(fm.create_path_string('application', 'monster_energy.jpg'))

#resize_img = tf.image.resize(img, (256, 256))
#predict = model.predict(np.expand_dims(resize_img/255, 0))
#print(predict)

#print(validation_data)