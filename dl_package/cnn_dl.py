# imports
import os
import numpy as np
# Importing load from json
from tensorflow.keras.models import model_from_json

# importing keras
from tensorflow import keras as keras


# initialize Deep learning
def cnn_deep_learning(image, parent_directory):

    """
    This function is used to import the CNN deep learning model and initialize it. it returns the predicted output form the image given in the form of (28, 28)
    :param image: 1*784 image shape
    :param parent_directory: its the relative diretory location where the main.py is located
    :return: returns the predicted output from the deep learning model
    """

    # converting image to numpy array
    numpy_image = np.asarray(image)

    # reshaping the image as per required input
    input_image = numpy_image.reshape((1, 28, 28, 1))

    # ------------LOADING DEEP LEARNING CNN MODEL-----------------
    json_save_loc = "models"
    json_model_filepath = os.path.join(parent_directory, json_save_loc, "digit_classifier_cnn_model.json")
    model_filepath = os.path.join(parent_directory, json_save_loc, "digit_classifier_cnn_weights.hdf5")

    # load json and create model
    with open(json_model_filepath, 'r') as json_file:
        loaded_model_json = json_file.read()

    # Loading Architecture of Model
    cnn_digit_val = model_from_json(loaded_model_json)

    # Loading weights of the Model
    cnn_digit_val.load_weights(model_filepath)

    # Compiling the loaded model
    cnn_digit_val.compile(loss=keras.losses.CategoricalCrossentropy(from_logits=True), optimizer=keras.optimizers.Adam(lr=1e-4), metrics=['acc', 'AUC'], )

    # Checking the arhitecture of the model
    # print(cnn_digit_val.summary())

    # predicting the image given in the input
    predicted_value = np.argmax(cnn_digit_val.predict(input_image))

    return predicted_value