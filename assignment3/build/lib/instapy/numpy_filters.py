"""numpy implementation of image filters"""

from cgitb import grey
from typing import Optional
import numpy as np

from PIL import Image
from instapy.io import display 


def numpy_color2gray(image: np.array) -> np.array:
    """Convert rgb pixel array to grayscale

    Args:
        image (np.array)
    Returns:
        np.array: gray_image
    """

    gray_image = np.empty_like(image)


    red = image[:, :, 0] * 0.21
    green = image[:, :, 1] * 0.72
    blue = image [:, :, 2] * 0.07

    sumrgb = (red + green + blue)
    
    gray_image[:, :, 0] = sumrgb
    gray_image[:, :, 1] = sumrgb
    gray_image[:, :, 2] = sumrgb
    

    # Hint: use numpy slicing in order to have fast vectorized code
    ...
    # Return image (make sure it's the right type!)
    
    gray_image = gray_image.astype("uint8")  
     
    return gray_image


def numpy_color2sepia(image: np.array, k: Optional[float] = 1) -> np.array:
    """Convert rgb pixel array to sepia

    Args:
        image (np.array)
        k (float): amount of sepia filter to apply (optional)

    The amount of sepia is given as a fraction, k=0 yields no sepia while
    k=1 yields full sepia.

    (note: implementing 'k' is a bonus task,
    you may ignore it for Task 9)

    Returns:
        np.array: sepia_image
    """

    #if not 0 <= k <= 1:
        # validate k (optional)
        #raise ValueError(f"k must be between [0-1], got {k=}")


    # define sepia matrix (optional: with `k` tuning parameter for bonus task 13)
    sepia_matrix = [
    [ 0.393, 0.769, 0.189],
    [ 0.349, 0.686, 0.168],
    [ 0.272, 0.534, 0.131],
    ]

    # HINT: For version without adaptive sepia filter, use the same matrix as in the pure python implementation
    # use Einstein sum to apply pixel transform matrix
    # Apply the matrix filter
    # Check which entries have a value greater than 255 and set it to 255 since we can not display values bigger than 255

    sepia_image = np.empty_like(image)


    r = image[:, :, 0] 
    g = image[:, :, 1] 
    b = image [:, :, 2] 

    red = np.minimum(255,(r * sepia_matrix[0][0]) + (g * sepia_matrix[0][1]) + (b * sepia_matrix[0][2]))
    green = np.minimum(255, (r *sepia_matrix[1][0]) + (g *sepia_matrix[1][1]) + (b * sepia_matrix[1][2]))
    blue = np.minimum(255, (r *sepia_matrix[2][0]) + (g *sepia_matrix[2][1]) + (b* sepia_matrix[2][2]))
    sepia_image[:, :, 0] = red
    sepia_image[:, :, 1] = green
    sepia_image[:, :, 2] = blue
    

    # Return image (make sure it's the right type!)

    sepia_image = sepia_image.astype("uint8")  

    return sepia_image

