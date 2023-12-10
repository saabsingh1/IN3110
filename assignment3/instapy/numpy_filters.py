"""numpy implementation of image filters"""

from typing import Optional
import numpy as np


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
    blue = image[:, :, 2] * 0.07

    sumrgb = (red + green + blue)

    gray_image[:, :, 0] = sumrgb
    gray_image[:, :, 1] = sumrgb
    gray_image[:, :, 2] = sumrgb

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
    """
    #if not 0 <= k <= 1:
        # validate k (optional)
        # raise ValueError(f"k must be between [0-1], got {k=}")
    """

    # define sepia matrix
    sepia_matrix = [[0.393, 0.769, 0.189],
                    [0.349, 0.686, 0.168],
                    [0.272, 0.534, 0.131]]

    sepia_image = np.empty_like(image)

    sepia_image = np.minimum(255, np.einsum("jki,li",image,sepia_matrix))

    # Return image (make sure it's the right type!)
    sepia_image = sepia_image.astype("uint8")

    return sepia_image
