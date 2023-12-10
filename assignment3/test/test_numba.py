from instapy.numba_filters import numba_color2gray, numba_color2sepia
import random
import numpy as np


def test_color2gray(image, reference_gray):
    testimage = numba_color2gray(image)
    assert testimage.shape == image.shape
    assert testimage.dtype == "uint8"
    assert testimage.dtype == image.dtype
    assert type(testimage) == np.ndarray
    assert np.allclose(testimage, reference_gray)

    sumrgb = (image[0][0][0] * 0.21 + image[0][0][1] * 0.72 + image[0][0][2] * 0.07)
    image[0][0] = (sumrgb, sumrgb, sumrgb)
    assert np.allclose(image[0][0], testimage[0][0])

    sumrgb2 = (image[10][10][0] * 0.21 + image[10][10][1] * 0.72 + image[10][10][2] * 0.07)
    image[10][10] = (sumrgb2, sumrgb2, sumrgb2)
    assert np.allclose(image[10][10], testimage[10][10])

    sumrgb3 = (image[15][15][0] * 0.21 + image[15][15][1] * 0.72 + image[15][15][2] * 0.07)
    image[15][15] = (sumrgb3, sumrgb3, sumrgb3)
    assert np.allclose(image[15][15], testimage[15][15])

    sumrgb4 = (image[22][22][0] * 0.21 + image[22][22][1] * 0.72 + image[22][22][2] * 0.07)
    image[22][22] = (sumrgb4, sumrgb4, sumrgb4)
    assert np.allclose(image[22][22], testimage[22][22])


def test_color2sepia(image, reference_sepia):
    testimage = numba_color2sepia(image)
    assert testimage.shape == image.shape
    assert testimage.dtype == "uint8"
    assert testimage.dtype == image.dtype
    assert type(testimage) == np.ndarray
    assert np.allclose(testimage, reference_sepia)

    sepia_matrix = [[0.393, 0.769, 0.189],
                    [0.349, 0.686, 0.168],
                    [0.272, 0.534, 0.131]]

    # checking some random rgb values
    for _ in range(10):
        x = random.randint(0, image.shape[0] - 1)
        y = random.randint(0, image.shape[1] - 1)

        s = image[x][y]
        r = s[0]
        g = s[1]
        b = s[2]

        red = min(255, (r * sepia_matrix[0][0]) + (g * sepia_matrix[0][1]) + (b * sepia_matrix[0][2]))
        green = min(255, (r * sepia_matrix[1][0]) + (g * sepia_matrix[1][1]) + (b * sepia_matrix[1][2]))
        blue = min(255, (r * sepia_matrix[2][0]) + (g * sepia_matrix[2][1]) + (b * sepia_matrix[2][2]))

        image[x][y] = (red, green, blue)
        assert np.allclose(image[x][y], testimage[x][y])
