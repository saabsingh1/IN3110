"""
Timing our filter implementations.

Can be executed as `python3 -m instapy.timing`

For Task 6.
"""
import time
from turtle import width
import instapy
import io 
from typing import Callable
import numpy as np
from PIL import Image

from instapy.numpy_filters import numpy_color2gray, numpy_color2sepia
from instapy.python_filters import python_color2gray, python_color2sepia
from instapy.numba_filters import  numba_color2gray, numba_color2sepia



def time_one(filter_function: Callable, *arguments, calls: int = 3) -> float:
    """Return the time for one call

    When measuring, repeat the call `calls` times,
    and return the average.

    Args:
        filter_function (callable):
            The filter function to time
        *arguments:
            Arguments to pass to filter_function
        calls (int):
            The number of times to call the function,
            for measurement
    Returns:
        time (float):
            The average time (in seconds) to run filter_function(*arguments)
    """
    # run the filter function `calls` times
    # return the _average_ time of one call
    totaltime = 0 
    for _ in range(calls):
        start = time.time() #vurder å bytt ut med time.perftimer()
        filter_function(arguments[0])
        end = time.time()
        diff = end - start 
        totaltime += diff
    averagetime = totaltime / calls
    return averagetime

def make_reports(filename: str = "test/rain.jpg", calls: int = 3):
    """
    Make timing reports for all implementations and filters,
    run for a given image.

    Args:
        filename (str): the image file to use
    """
    # load the image
    imagearray = np.asarray(Image.open(filename))
    image = Image.fromarray(imagearray)
    # print the image name, width, height
    print("Timing performed using", filename + ":", image.width, "x", image.height)
    # iterate through the filters
    filter_names = ["color2gray", "color2sepia"]
    for filter_name in filter_names:
        # get the reference filter function
        # time the reference implementation
        reference_time = 0
        reference_filter = filter_name
        if reference_filter == "color2gray":
            reference_time = time_one(python_color2gray, imagearray)
        elif reference_filter =="color2sepia": 
            reference_time = time_one(python_color2sepia,imagearray)        
        
        print(
            f"Reference (pure Python) filter time {filter_name}: {reference_time:.3}s ({calls=})"
        )
        # iterate through the implementations
        implementations = ["numpy", "numba"]
        for implementation in implementations:
            filter = implementation
            filter_time = 0
            if filter_name.__eq__("color2gray") and filter.__eq__("numpy"):
                filter_time = time_one(numpy_color2gray, imagearray)
            elif filter_name.__eq__("color2gray") and filter.__eq__("numba"):
                filter_time = time_one(numba_color2gray, imagearray)
            elif filter_name.__eq__("color2sepia") and filter.__eq__("numpy"):
                filter_time = time_one(numpy_color2sepia, imagearray)
            elif filter_name.__eq__("color2sepia") and filter.__eq__("numba"):
                filter_time = time_one(numba_color2sepia, imagearray)
            # compare the reference time to the optimized time
            speedup = (reference_time/filter_time) 
            print(
                f"Timing: {implementation} {filter_name}: {filter_time:.3}s ({speedup=:.2f}x)"
            )


if __name__ == "__main__":
    # run as `python -m instapy.timing`
    make_reports()
