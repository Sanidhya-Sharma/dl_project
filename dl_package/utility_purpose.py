import os
from sys import platform
import base64
import hashlib
import random

def create_saved_folder(parent_directory):
    """
    This function is used to create "saved" folder in the current working directory given sa the input to the function
    :param parent_directory: relative current directory where you want the "saved" folder to be created
    :return: Bool (True/False)
    """
    # Reference before assigment
    create_path = ""
    diretory_path = ""

    if platform == "linux" or platform == "linux2":
        diretory_path = "" + parent_directory + "/saved"
        isExist = os.path.exists(diretory_path)

        if isExist:
            pass
        else:
            create_directory_path = diretory_path
            new_directory_lst = create_directory_path.split("/")
            new_directory = new_directory_lst[-1]

            create_path = os.path.join(parent_directory, new_directory)
            os.mkdir(create_path)

    elif platform == "darwin":
        diretory_path = "" + parent_directory + "/saved"
        isExist = os.path.exists(diretory_path)

        if isExist:
            pass
        else:
            create_directory_path = diretory_path
            new_directory_lst = create_directory_path.split("/")
            new_directory = new_directory_lst[-1]

            create_path = os.path.join(parent_directory, new_directory)
            os.mkdir(create_path)

    elif platform == "win32":
        diretory_path = "" + parent_directory + "\saved"
        isExist = os.path.exists(diretory_path)

        if isExist:
            pass
        else:
            create_directory_path = diretory_path
            new_directory_lst = create_directory_path.split("\\")
            new_directory = new_directory_lst[-1]

            create_path = os.path.join(parent_directory, new_directory)
            os.mkdir(create_path)

    if isExist == True:
        created = False
        create_path = diretory_path
    else:
        created = True
        create_path = create_path

    return created, create_path

def request_base64_extractor(responce):
    """
    This function is used to extract a JSON responce of a base64 image posted from the Front-End and extract the base 64 string
    Eg : data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABwA…VcCqfQzW0rVAtSrtQ45H+ACOAIR1U59zQAAAAAElFTkSuQmCC --> iVBORw0KGgoAAAANSUhEUgAAABwA…VcCqfQzW0rVAtSrtQ45H+ACOAIR1U59zQAAAAAElFTkSuQmCC
    :param responce: JSON stringify
    :return: base64 (string)
    """
    # Convert to list
    responce_to_list = responce["image_base64"].split(",")

    # Grab base64 code only from list from lsat
    base64_image = responce_to_list[-1]

    return base64_image

# Generate Hash key
def generate_hash_key():
    """
    @return: A hashkey for use to authenticate agains the API.
    """
    return hashlib.sha256(str(random.getrandbits(256)).encode('utf-8')).hexdigest()

# Get the application key
def get_app_key(loc :str):
    """
    This function is used to provide app key
    :param location : (Str) location of env file
    :return: (Str) the app key
    """
    with open(str(loc), 'r') as apikey:
        key = apikey.read().replace('\n', '')
    return key

def base64_encoder(key):
    """
    This function is used to provide base64 encrypting for an input string
    :param key : (Str) any input string
    :return: (Str) base64 encrypted key
    """
    input_key = key
    utf8_key = input_key.encode("utf-8")
    encoded = base64.b64encode(utf8_key)
    encoded_utf8_key = encoded.decode("utf-8")
    return encoded_utf8_key

def base64_decoder(key):
    """
    This function is used to provide base64 decryption for an input string
    :param key : (Str) any input string base64
    :return: (Str) base64 decrypted key
    """
    input_key = bytes(key, 'UTF-8')
    decoded = base64.b64decode(input_key)
    decoded_utf8_key = decoded.decode("utf-8")
    return decoded_utf8_key
