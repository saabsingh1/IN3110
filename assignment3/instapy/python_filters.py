"""pure Python implementation of image filters"""

import numpy as np


def python_color2gray(image: np.array) -> np.array:
    """Convert rgb pixel array to grayscale

    Args:
        image (np.array)
    Returns:
        np.array: gray_image
    """
    gray_image = np.empty_like(image)
    # iterate through the pixels, and apply the grayscale transform

    for row, greyrow in zip(image, gray_image):
        for rgb, greyrgb in zip(row, greyrow):
            red = rgb[0] * 0.21
            green = rgb[1] * 0.72
            blue = rgb[2] * 0.07

            sumrgb = red + green + blue

            greyrgb[0] = sumrgb
            greyrgb[1] = sumrgb
            greyrgb[2] = sumrgb

    gray_image = gray_image.astype("uint8")
    return gray_image


def python_color2sepia(image: np.array) -> np.array:
    """Convert rgb pixel array to sepia

    Args:
        image (np.array)
    Returns:
        np.array: sepia_image
    """

    # Iterate through the pixels
    # applying the sepia matrix

    sepia_matrix = [[0.393, 0.769, 0.189],
                    [0.349, 0.686, 0.168],
                    [0.272, 0.534, 0.131]]

    H, W, _ = image.shape

    sepia_image = np.empty((H, W, 3))

    for h in range(H):
        for w in range(W):
            s = image[h][w]
            r = s[0]
            g = s[1]
            b = s[2]

            red = min(255, (r * sepia_matrix[0][0]) + (g * sepia_matrix[0][1]) + (b * sepia_matrix[0][2]))
            green = min(255, (r *sepia_matrix[1][0]) + (g *sepia_matrix[1][1]) + (b * sepia_matrix[1][2]))
            blue = min(255, (r *sepia_matrix[2][0]) + (g *sepia_matrix[2][1]) + (b* sepia_matrix[2][2]))

            sepia_image[h][w] = (red, green, blue)

    # Return image
    # don't forget to make sure it's the right type!
    sepia_image = sepia_image.astype("uint8")

    return sepia_image
