import cv2
import numpy as np
import os
import sys
import tensorflow as tf
from keras.models import *
from keras.layers import *
from sklearn.model_selection import *

from sklearn.model_selection import train_test_split

EPOCHS = 10
IMG_WIDTH = 30
IMG_HEIGHT = 30
NUM_CATEGORIES = 43
TEST_SIZE = 0.4


def main():
    print(tf.__version__)

    # Check command-line arguments
    if len(sys.argv) not in [2, 3]:
        sys.exit("Usage: python traffic.py data_directory [model.h5]")

    # Get image arrays and labels for all image files
    images, labels = load_data(sys.argv[1])

    # Split data into training and testing sets
    labels = tf.keras.utils.to_categorical(labels)
    x_train, x_test, y_train, y_test = train_test_split(
        np.array(images), np.array(labels), test_size=TEST_SIZE
    )

    # Get a compiled neural network
    model = get_model()

    # Fit model on training data
    model.fit(x_train, y_train, epochs=EPOCHS)

    # Evaluate neural network performance
    model.evaluate(x_test,  y_test, verbose=2)

    # Save model to file
    if len(sys.argv) == 3:
        filename = sys.argv[2]
        model.save(filename)
        #print(f"Model saved to {filename}.")


def load_data(data_dir):
    """
    Load image data from directory `data_dir`.

    Assume `data_dir` has one directory named after each category, numbered
    0 through NUM_CATEGORIES - 1. Inside each category directory will be some
    number of image files.

    Return tuple `(images, labels)`. `images` should be a list of all
    of the images in the data directory, where each image is formatted as a
    numpy ndarray with dimensions IMG_WIDTH x IMG_HEIGHT x 3. `labels` should
    be a list of integer labels, representing the categories for each of the
    corresponding `images`.
    """
    images = list()
    labels = list()
    # iterate over all images inside subdirectories inside of data_dir
    for directoryPath, notUsed, fileNames in os.walk(data_dir):
        for file in fileNames:
            # read image into array and resize to preset width and height
            image = cv2.imread(os.path.join(directoryPath, file))
            if image is not None:
                resized = cv2.resize(image, (IMG_WIDTH, IMG_HEIGHT))
                label = int(os.path.basename(directoryPath))
                images.append(resized)
                labels.append(label)
    return images, labels


def get_model():
    """
    Returns a compiled convolutional neural network model. Assume that the
    `input_shape` of the first layer is `(IMG_WIDTH, IMG_HEIGHT, 3)`.
    The output layer should have `NUM_CATEGORIES` units, one for each category.
    """
    model = Sequential(
        [

            #convolutional layer + pooling (can be done many times in this order)
            Conv2D(200, (8, 8), activation="relu", input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)),
            MaxPooling2D(pool_size=(2, 2)),
            Conv2D(250, (4, 4), activation="relu"),
            MaxPooling2D(pool_size=(2, 2)),
            Conv2D(250, (2, 2), activation="relu"),
            MaxPooling2D(pool_size=(2, 2)),

            # turn multidimensional input into one dimensional
            Flatten(),

            # add dense layer with relu activation
            Dense(450, activation="relu"),

            # dropout of 0.5 to not rely too much on certain nodes
            Dropout(0.5),

            # add dense layer with softmax activation
            Dense(NUM_CATEGORIES, activation="softmax"),

        ]
    )
    # summary
    model.summary()
    # compile
    model.compile(optimizer= "adam", loss = "categorical_crossentropy", metrics=["accuracy"])
    # return
    return model


if __name__ == "__main__":
    main()