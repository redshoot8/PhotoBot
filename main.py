import tensorflow as tf
from tensorflow import keras
import numpy as np
import matplotlib.pyplot as plt

dataset = keras.datasets.cifar10
(train_images, train_labels), (test_images, test_labels) = dataset.load_data()

class_names = [
    'airplane',
    'automobile',
    'bird',
    'cat',
    'deer',
    'dog',
    'frog',
    'horse',
    'ship',
    'truck'
]

print(train_images.shape)  # 50000 images 32x32

print(test_images.shape)  # 10000 images 32x32

print(len(train_labels))  # 50000

print(len(test_labels))  # 10000

print(train_labels)  # int numbers (0 - 9)

plt.figure()
plt.imshow(train_images[0])
plt.colorbar()
plt.grid(False)



