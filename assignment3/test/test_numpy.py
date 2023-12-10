from instapy.numpy_filters import numpy_color2gray, numpy_color2sepia
import numpy as np
import random


def test_color2gray(image, reference_gray):
    testimage = numpy_color2gray(image)
    assert testimage.shape == image.shape
    assert testimage.dtype == "uint8"
    assert testimage.dtype == image.dtype
    assert type(testimage) == np.ndarray
    assert np.allclose(testimage, reference_gray, atol=1)

    for _ in range(10):
        x = random.randint(0, image.shape[0]-1)
        y = random.randint(0, image.shape[1]-1)

        red = image[x, y, 0] * 0.21
        green = image[x, y, 1] * 0.72
        blue = image[x, y, 2] * 0.07

        sumrgb = (red + green + blue)

        image[x, y, 0] = sumrgb
        image[x, y, 1] = sumrgb
        image[x, y, 2] = sumrgb
        assert np.allclose(image[x][y], testimage[x][y], atol=1)


def test_color2sepia(image, reference_sepia):
    testimage = numpy_color2sepia(image)
    assert testimage.shape == image.shape
    assert testimage.dtype == "uint8"
    assert testimage.dtype == image.dtype
    assert type(testimage) == np.ndarray
    assert np.allclose(testimage, reference_sepia, atol=1)

    sepia_matrix = [[0.393, 0.769, 0.189],
                    [0.349, 0.686, 0.168],
                    [0.272, 0.534, 0.131]]

    for _ in range(10):
        x = random.randint(0, image.shape[0]-1)
        y = random.randint(0, image.shape[1]-1)

        r = image[x, y, 0]
        g = image[x, y, 1]
        b = image[x, y, 2]

        red = np.minimum(255, (r * sepia_matrix[0][0]) + (g * sepia_matrix[0][1]) + (b * sepia_matrix[0][2]))
        green = np.minimum(255, (r * sepia_matrix[1][0]) + (g * sepia_matrix[1][1]) + (b * sepia_matrix[1][2]))
        blue = np.minimum(255, (r * sepia_matrix[2][0]) + (g * sepia_matrix[2][1]) + (b * sepia_matrix[2][2]))
        image[x, y, 0] = red
        image[x, y, 1] = green
        image[x, y, 2] = blue
        assert np.allclose(image[x][y], testimage[x][y], atol=1)
