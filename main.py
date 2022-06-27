# Global Imports
from flask import Flask, render_template, request, url_for, redirect, jsonify, send_from_directory, g, session
import os
from functools import wraps

# CSRF
from flask_wtf.csrf import CSRFProtect, CSRFError, generate_csrf

# Logging
import logging
from logging.handlers import TimedRotatingFileHandler
from logging import Formatter

# Image processing imports
from PIL import Image
import base64

# DS imports
import numpy as np

# Local Custom Packages Import
import dl_package as dlpckg

# -importing the models-
# import pickle
# model_filename = "lr_c32.pkl"
# lr = pickle.load(open("./models/"+model_filename+"", 'rb'))

# Self Signed SSL
import ssl
context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
context.load_cert_chain('creds/ssl/cert.pem', 'creds/ssl/key.pem')

# Initialize app
app = Flask(__name__, static_folder='static', template_folder="templates")

# Token expire after 5 min
app.config['WTF_CSRF_TIME_LIMIT'] = 300

# Reload CSS and JS files and Not cache them
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# app.config['SERVER_NAME'] = os.environ['MY_SERVER_NAME']

# Initialize CSRF
csrf = CSRFProtect(app)
csrf.init_app(app)

# Temp key
appKey = None
tempKey = None

# Custom Key for CSRF
app.config.update(dict(
    SECRET_KEY=dlpckg.get_app_key(loc=""+os.getcwd()+""+os.sep+"creds"+os.sep+"apikey"+os.sep+"api.key"),
    WTF_CSRF_SECRET_KEY=dlpckg.generate_hash_key()
))

# Image folder
PEOPLE_FOLDER = os.path.join('static', 'img')
app.config['UPLOAD_FOLDER'] = PEOPLE_FOLDER


# CUSTOM WRAPPER (Dual Key)
# The actual decorator function for checking the api Key for require_appkey wrapper
def require_appkey_tempKey(view_function):
    @wraps(view_function)
    # the new, post-decoration function. Note *args and **kwargs here.
    def decorated_function(*args, **kwargs):

        # storing in key
        key = dlpckg.get_app_key(loc=""+os.getcwd()+""+os.sep+"creds"+os.sep+"apikey"+os.sep+"api.key")

        # Storing the received keys in header
        recieved_api_key = request.headers.get('x-api-key')
        recieved_temp_key = request.headers.get('temp-key')

        # Decode the base64
        decoded_api_key = dlpckg.base64_decoder(recieved_api_key)
        decoded_temp_key = dlpckg.base64_decoder(recieved_temp_key)

        # URL BreakDown
        origin_url = request.headers["Origin"]
        base_url = request.headers["Referer"].rsplit('/', 1)[0]
        endpoint_url = request.headers["Referer"].rsplit('/', 1)[1]

        # Global Variables
        global appKey
        global tempKey

        # Check if the input x-api-key matches the apiKey
        # if request.args.get('key') and request.args.get('key') == key:
        # if request.headers.get('x-api-key') and request.headers.get('x-api-key') == key:
        if decoded_temp_key == tempKey and decoded_api_key == key:
            app.logger.info("Dual keys Verified")

            # I had to do this
            if appKey and tempKey is not None:
                appKey = decoded_api_key
                tempKey = decoded_temp_key

            return view_function(*args, **kwargs)
        else:
            app.logger.error("Dual keys Verification failed")
            return jsonify({"data": "Failed Key Authorization", "code": "401", "redirect_url": ""+base_url+""+url_for("not_found_error")+"", 'success': False})

    return decorated_function


# Providing static folder
@app.route('/<path:filename>')
def send_file(filename):
    return send_from_directory(app.static_folder, filename)

# Custom Function
def deep_learning_model_init():

    # Relative parent directory
    parent_directory = os.getcwd()

    # Dummy white image for initialization
    dummy_image = np.full((28, 28, 1), 255, dtype=np.uint8)

    # Initialization for Sequential Dense deep learning model
    dlpckg.sequential_dense_deep_learning(image=dummy_image, parent_directory=parent_directory)

    # Logs
    app.logger.info("Initialized Sequential Dense model For first time")

    # Initialization for CNN deep learning model
    dlpckg.cnn_deep_learning(image=dummy_image, parent_directory=parent_directory)

    # Logs
    app.logger.info("Initialized CNN + Dense model For first time")


# ----------------Routes--------------------

# Logging
@app.before_first_request
def before_first_request():

    # Setting log level
    log_level = logging.INFO

    # Removing Handlers
    for handler in app.logger.handlers:
        app.logger.removeHandler(handler)

    # Log directory path
    root = os.path.dirname(os.path.abspath(__file__))
    log_dir_path = os.path.join(root, 'logs')

    # Check if the "logs" directory is available at root directory if not create one
    if not os.path.exists(log_dir_path):
        os.mkdir(log_dir_path)

    # Log File path
    log_file = os.path.join(log_dir_path, 'app.log')

    # Default handler
    # handler = logging.FileHandler(log_file)

    # Time Rotating handler
    handler = TimedRotatingFileHandler(filename=log_file, when='H', interval=1, backupCount=1, encoding='utf-8', delay=False)

    # Create formatter and add to handler
    FORMATTER = Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(FORMATTER)

    # Adding log handlers
    app.logger.addHandler(handler)

    # Setting log level (default INFO)
    app.logger.setLevel(log_level)

    # Logging
    app.logger.info("Logs Initialized")

    # Global Super key
    global tempKey
    tempKey = dlpckg.generate_hash_key()

    # App key Setup
    key = dlpckg.get_app_key(loc=""+os.getcwd()+""+os.sep+"creds"+os.sep+"apikey"+os.sep+"api.key")
    global appKey
    appKey = key


@app.route("/keyValuesCalls", methods=["GET"])
def get_keys():
    # POST request
    if request.method == 'GET':

        keys = {
            'x-api-key': dlpckg.base64_encoder(appKey),
            'temp-key': dlpckg.base64_encoder(tempKey)
        }
    return jsonify(keys)

# Default Route
@app.route("/", methods=["GET"])
def home():
    if request.method == 'GET':
        # Logs
        app.logger.info("Browsed for Home Page")

        # flag for navbar
        include_nav = True

        # Flag for footer
        include_footer = True

    return render_template('home.html', include_nav=include_nav, include_footer=include_footer)

# Navigation Page
@app.route("/navigation", methods=["GET"])
def navigation():
    if request.method == 'GET':
        # Logs
        app.logger.info("Browsed for Navigation Page")

        # flag for navbar
        include_nav = True

        # Flag for footer
        include_footer = True

    return render_template('navigation.html', include_nav=include_nav, include_footer=include_footer)

# Canvas Page
@app.route("/canvas", methods=["GET"])
def canvas():
    if request.method == 'GET':
        # initialize the Deep learning Models (Commented as there is already a JS function responsible)
        # deep_learning_model_init()

        # Logs
        app.logger.info("Browsed for Canvas Page")

        # Flag for navbar
        include_nav = False

        # Flag for footer
        include_footer = False

        # Deep learning Model List
        deep_learning_model_dict = {"Sequential Dense Model (4 layer 2 Hidden)": "Dense", "CNN (7 layer Conv2D + 1 Dense)": "CNN"}

    return render_template('canvas.html', include_nav=include_nav, include_footer=include_footer, deep_learning_model_dict=deep_learning_model_dict)

# Canvas Page
@app.route("/dl_initialization", methods=["GET", "POST"])
@csrf.exempt
@require_appkey_tempKey
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

            # Logs
            app.logger.info("DL initialized ran OK")

            # returning prediction via AJAX
            resp = jsonify(success=True, status=200, data=str("Deep Learning Models initialized"))

            return resp, 200

        except Exception as e:

            # Logs
            app.logger.error("DL initialization failed with error : "+str(e)+"")

            # returning prediction via AJAX
            resp = jsonify(success=False, status=500, data=str("Deep Learning Models unable to initialize"))

            return resp, 500

# Deep learning Results Endpoint
@app.route("/result", methods=["GET", "POST"])
@csrf.exempt
@require_appkey_tempKey
def result():

    # GET request
    if request.method == 'GET':
        return redirect(url_for('error401'))

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

            # Getting channels of the inverted image
            img_dim_inv = dlpckg.image_info(invert_color_image, saved_folder_location)[2]

            # convert to gray scale
            gray_scale_image = dlpckg.convert_to_grayscale(invert_color_image, saved_folder_location, img_dim_inv)

            # final image preprocessed
            final_image = Image.open(f'saved/{gray_scale_image}')

            # Predicting values using sequential Deep learning
            if requested_architecture == "CNN":
                prediction = dlpckg.cnn_deep_learning(final_image, parent_directory)

                # Logs
                app.logger.info("Prediction called for CNN")

            elif requested_architecture == "Dense":
                prediction = dlpckg.sequential_dense_deep_learning(final_image, parent_directory)

                # Logs
                app.logger.info("Prediction called for Sequential Dense")

            else:
                prediction = "No Architecture Selected"

                # Logs
                app.logger.info("Prediction not called as architecture was not provided")

            # returning prediction via AJAX
            resp = jsonify(success=True, status=200, data=str(prediction))

            # Logs
            app.logger.info("Prediction Result ran OK")

            return resp, 200

        except Exception as e:

            resp = jsonify(success=False, status=404, exception="Error Saving the file due to Error : "+str(e)+"")

            # Logs
            app.logger.error("Prediction Result Failed with error : "+str(e)+"")

            return resp, 404

# CSRF Error route
@app.route("/errorCSRF", methods=["GET"])
def csrf_error():
    if request.method == 'GET':
        # Logs
        app.logger.info("Shown the CSRF Error Page")

        # Location of the image in static folder
        full_filename_image = os.path.join(app.config['UPLOAD_FOLDER'], 'hacker.png')

        description = "The CSRF Tokens don't match"

        return render_template('errorCSRF.html', reason=description, hacker_img=full_filename_image)

# Error 404 route
@app.route("/error401", methods=["GET"])
def not_found_error():
    if request.method == 'GET':
        # Logs
        app.logger.info("Shown the Error 404 Page")

        return render_template('error401.html'), 401


@app.before_request
def header_check():
    if request.method == 'POST':

        # URL BreakDown
        origin_url = request.headers["Origin"]
        base_url = request.headers["Referer"].rsplit('/', 1)[0]
        endpoint_url = request.headers["Referer"].rsplit('/', 1)[1]

        if request.cookies.get('csrf_token') == request.headers["X-CSRFToken"]:
            app.logger.info("before Request CSRF verified")
        else:
            # Logs
            app.logger.warn("before Request CSRF not verified")

            return jsonify({"data": "Failed CSRF Authorization", "code": "403", "redirect_url": ""+base_url+""+url_for("csrf_error")+"", 'success': False}), 403

@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    response.headers['Cache-Control'] = 'public, max-age=0'

    # Inject new CSRF in cookie
    response.set_cookie('csrf_token', generate_csrf())

    # Sending Keys
    response.set_cookie('ak', dlpckg.base64_encoder(appKey))
    response.set_cookie('tk', dlpckg.base64_encoder(tempKey))

    return response


# CSRF ERROR PAGE
@app.errorhandler(CSRFError)
def handle_csrf_error(e):
    # Logs
    app.logger.error("CSRF ERROR : "+str(e)+" ")

    return jsonify({"data": "Failed CSRF Security Authorization", "code": "403", "redirect_url": ""+url_for("csrf_error")+"", 'success': False}), 403

