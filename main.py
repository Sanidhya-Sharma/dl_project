# Global Imports
from flask import Flask, render_template, request, url_for, redirect, jsonify
import os
from PIL import Image
from numpy import asarray
import numpy as np

# Local Custom Packages Import
import dl_package as dlpckg

# -importing the models-
# import pickle
# model_filename = "lr_c32.pkl"
# lr = pickle.load(open("./models/"+model_filename+"", 'rb'))

# initialize app
app = Flask(__name__)


# Custom Function
def deep_learning_model_init():

    # Relative parent directory
    parent_directory = os.getcwd()

    # Dummy white image for initialization
    dummy_image = np.full((28, 28, 1), 255, dtype=np.uint8)

    # Initialization for Sequential Dense deep learning model
    dlpckg.sequential_dense_deep_learning(image=dummy_image, parent_directory=parent_directory)
    print("Initialized Sequential Dense model")

    # Initialization for CNN deep learning model
    dlpckg.cnn_deep_learning(image=dummy_image, parent_directory=parent_directory)
    print("Initialized CNN + Dense model")


# ----------------Routes--------------------


# Default Route
@app.route("/", methods=["GET"])
def home():

    # flag for navbar
    include_nav = True
    # Flag for footer
    include_footer = True

    return render_template('home.html', include_nav=include_nav, include_footer=include_footer)

# Navigation Page
@app.route("/navigation", methods=["GET"])
def navigation():

    # flag for navbar
    include_nav = True
    # Flag for footer
    include_footer = True

    return render_template('navigation.html', include_nav=include_nav, include_footer=include_footer)

# Canvas Page
@app.route("/canvas", methods=["GET"])
def canvas():

    # initialize the Deep learning Models
    # deep_learning_model_init()

    # Flag for navbar
    include_nav = False

    # Flag for footer
    include_footer = False

    deep_learning_model_dict = {"Sequential Dense Model (4 layer 2 Hidden)" : "Dense", "CNN (7 layer Conv2D + 1 Dense)" : "CNN"}

    return render_template('canvas.html', include_nav=include_nav, include_footer=include_footer, deep_learning_model_dict=deep_learning_model_dict)

# Canvas Page
@app.route("/dl_initialization", methods=["GET", "POST"])
def dl_initialization():

    # GET request
    if request.method == 'GET':
        return render_template("canvas.html")

    # POST request
    if request.method == 'POST':

        try:
            # initialize the Deep learning Models
            deep_learning_model_init()

            # Checking failing case
            # assert "birthday cake" == "ice cream cake", "Should've asked for pie"

            # returning prediction via AJAX
            resp = jsonify(success=True, status=200, data=str("Deep Learning Models initialized"))

            return resp

        except Exception as e:

            # returning prediction via AJAX
            resp = jsonify(success=False, status=500, data=str("Deep Learning Models unable to initialize"))

            return resp

# Deep learning Results Endpoint
@app.route("/result", methods=["GET", "POST"])
def result():

    # GET request
    if request.method == 'GET':
        return render_template("canvas.html")

    # POST request
    if request.method == 'POST':
        try:
            # Grabing the JSON Base64 stringyfy
            posted_image = request.get_json()

            requested_architecture = posted_image["architecture"]

            # Grab base64 code only from list
            base64_image = dlpckg.request_base64_extractor(posted_image)

            # Getting current working directory
            parent_directory = os.getcwd()

            # Checking platform and making directory "Saved"
            saved_folder_created_bool, saved_folder_location = dlpckg.create_saved_folder(parent_directory)

            # Decoding input from base64 to image
            decoded_image = dlpckg.decode_base64_to_image(base64_image)

            # saving the decoded image
            saved_decoded_base64_image = dlpckg.save_decoded_base64_image(decoded_image, saved_folder_location)

            # Adding white background
            white_background_image = dlpckg.add_white_background(saved_decoded_base64_image, saved_folder_location)

            # invert image colors
            invert_color_image = dlpckg.invert_colors(white_background_image, saved_folder_location)

            # convert to gray scale
            gray_scale_image = dlpckg.convert_to_grayscale(invert_color_image, saved_folder_location)

            # final image preprocessed
            final_image = Image.open(f'saved/{gray_scale_image}')

            # Predicting values using sequential Deep learning
            if requested_architecture == "CNN":
                prediction = dlpckg.cnn_deep_learning(final_image, parent_directory)
                print("Ran CNN")

            elif requested_architecture == "Dense":
                prediction = dlpckg.sequential_dense_deep_learning(final_image, parent_directory)
                print("Ran Dense")
            else:
                prediction = "No Architecture Selected"
                print("Ran Nothing")

            # returning prediction via AJAX
            resp = jsonify(success=True, status=200, data=str(prediction))

            return resp

        except Exception as e:

            resp = jsonify(success=False, status=404, exception="Error Saving the file due to Error : "+e+"")

            return resp
