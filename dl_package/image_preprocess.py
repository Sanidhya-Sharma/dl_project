# Imports
import base64
from PIL import Image, ImageChops
import cv2
import numpy as np


def decode_base64_to_image(base64_code_input):
    # Convert base64 to UTF8 format
    cleaned_image = base64_code_input.encode("utf-8")

    # Decode base64 to image
    decoded_image = base64.b64decode(cleaned_image)

    return decoded_image


def encode_image_to_base64(image_input):
    # Convert base64 to UTF8 format
    cleaned_input_image = image_input.encode("utf-8")

    # Convert base64 to base64
    encoded_image = base64.b64encode(cleaned_input_image)

    return encoded_image


def save_decoded_base64_image(decoded_base64, saved_folder_location):
    # Converting and writing
    with open(f"{saved_folder_location}/saved_writing.jpg", "wb") as fh:
        fh.write(decoded_base64)
    saved_image_name = "saved_writing.jpg"

    return saved_image_name


def add_white_background(image_name, saved_folder_location):
    # Adding white background and saving
    img_pillow = Image.open(f"{saved_folder_location}/{image_name}")
    new_image = Image.new("RGBA", img_pillow.size, "WHITE")  # Create a white rgba background
    new_image.paste(img_pillow, (0, 0), img_pillow)  # Paste the image on the background
    new_image.convert('RGB').save(f'{saved_folder_location}/prepros_wht_bck.jpg', "JPEG")  # Save as JPEG
    saved_image_name = 'prepros_wht_bck.jpg'

    return saved_image_name


def invert_colors(image_name, saved_folder_location):

    # inverting colours and saving
    img = Image.open(f'{saved_folder_location}/{image_name}')
    inv_img = ImageChops.invert(img)
    inv_img.convert('RGB').save('saved/prepros_inv.jpg', "JPEG")  # Save as JPEG
    saved_image_name = "prepros_inv.jpg"

    return saved_image_name


def convert_to_grayscale(image_name, saved_folder_location):

    # Converting to gray scale and normalizing the image
    cv_img = cv2.imread(f'{saved_folder_location}/{image_name}', 3)
    gray_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
    cv2.imwrite('saved/gray_scaled.jpg', gray_image)
    saved_image_name = "gray_scaled.jpg"

    return saved_image_name

def minmax_normalizer(image_name, saved_folder_location):

    # Reading the saved image
    input_image = Image.open(f'{saved_folder_location}/{image_name}')

    # Convert image to a numpy array
    numpy_image = np.asarray(input_image)

    # -Converting numpy array to float (make sure to convert back to uint8 before saving to image)-
    numpy_image = numpy_image.astype('float32')

    # -Min Max Normalization-
    numpy_image = (numpy_image - numpy_image.min())/(numpy_image.max() - numpy_image.min())

    # -Saving the image-
    normalized_image_conv = numpy_image.astype(np.uint8)
    normalized_image = Image.fromarray(normalized_image_conv)
    normalized_image.save(f"{saved_folder_location}/normalized_image.jpg")
    saved_image_name = "normalized_image.jpg"

    return saved_image_name