# Imports for image pre-processing
import base64
from PIL import Image, ImageChops
import cv2
import numpy as np
from numpy import asarray

# Gets the infomation of the given image
def image_info(image_name, saved_folder_location):

    """
    This is used to find the image information
    :param image_name: Stored image name (str)
    :param saved_folder_location: location of stored image (str)
    :return: image width, height and dimentions (Truple)
    """

    img = Image.open(f'{saved_folder_location}/{image_name}')
    img_np = asarray(img)
    img_info = img_np.shape

    return img_info

# Converts base64 to image
def decode_base64_to_image(base64_code_input):
    '''
    This function is used to convert the input base64 code to binary data format.

    The Base64 character set contains:
        26 uppercase letters
        26 lowercase letters
        10 numbers
        + and / for new lines (some implementations may use different characters)

    When the computer converts Base64 characters to binary, each Base64 character represents 6 bits of information.

    :param base64_code_input: base64 string (64 Characters)
    :return: Binary Data of image (Binary Data)
    '''

    # Convert base64 to UTF8 format
    cleaned_image = base64_code_input.encode("utf-8")

    # Decode base64 to image
    decoded_image = base64.b64decode(cleaned_image)

    return decoded_image

# Converts image to base64
def encode_image_to_base64(image_input):
    """
    This function helps encode a given binary image data input to base64.

    :param image_input: image string (str)
    :return: stored image name (str)
    """

    # Convert base64 to UTF8 format
    cleaned_input_image = image_input.encode("utf-8")

    # Convert base64 to base64
    encoded_image = base64.b64encode(cleaned_input_image)

    return encoded_image

# Saves the decoded image to specified location
def save_decoded_base64_image(decoded_base64, saved_folder_location):
    """
    This function helps to save a decoded image from base64 to binary image data to the desired location.

    :param decoded_base64: Binary Data of image (Binary Data)
    :param saved_folder_location: location to save the file to
    :return: stored image name (str)
    """

    # Converting and writing
    with open(f"{saved_folder_location}/saved_writing.jpg", "wb") as fh:
        fh.write(decoded_base64)
    saved_image_name = "saved_writing.jpg"

    return saved_image_name

# Adds white background to the image (Images which are with transparent background)
def add_white_background(image_name, saved_folder_location):
    """
    This function helps to add a white background to a given image.

    :param image_name: Stored image name (str)
    :param saved_folder_location: location of stored image (str)
    :return: stored image name (str)
    """

    # Adding white background and saving
    img_pillow = Image.open(f"{saved_folder_location}/{image_name}")
    new_image = Image.new("RGBA", img_pillow.size, "WHITE")  # Create a white rgba background
    new_image.paste(img_pillow, (0, 0), img_pillow)  # Paste the image on the background
    new_image.convert('RGB').save(f'{saved_folder_location}/prepros_wht_bck.jpg', "JPEG")  # Save as JPEG
    saved_image_name = 'prepros_wht_bck.jpg'

    return saved_image_name

# Inverts the color of the image (black --> White and White --> black)
def invert_colors(image_name, saved_folder_location):
    """
    This function inverts the colour of the given image.

    :param image_name: Stored image name (str)
    :param saved_folder_location: location of stored image (str)
    :return: stored image name (str)
    """

    # inverting colours and saving
    img = Image.open(f'{saved_folder_location}/{image_name}')
    inv_img = ImageChops.invert(img)
    inv_img.convert('RGB').save('saved/prepros_inv.jpg', "JPEG")  # Save as JPEG
    saved_image_name = "prepros_inv.jpg"

    return saved_image_name

# Converts the image to grayscale
def convert_to_grayscale(image_name, saved_folder_location, no_of_channels=3):
    """
    This function converts the given image to Gray Scale.

    :param image_name: Stored image name (str)
    :param saved_folder_location: location of stored image (str)
    :param no_of_channels: Number of channels of image (int) (defaults to 3)
    :return: stored image name (str)
    """

    # Converting to gray scale and normalizing the image
    cv_img = cv2.imread(f'{saved_folder_location}/{image_name}', no_of_channels)
    gray_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
    cv2.imwrite('saved/gray_scaled.jpg', gray_image)
    saved_image_name = "gray_scaled.jpg"

    return saved_image_name

# Normalizes the image of (0-255) to (0-1) using MinMax technique
def minmax_normalizer(image_name, saved_folder_location):
    """
    This function is used to perform a MinMax Normalization on the given input image making from 0-255 to 0-1.

    :param image_name: Stored image name (str)
    :param saved_folder_location: location of stored image (str)
    :return: stored image name (str)
    """

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