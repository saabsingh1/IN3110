"""Command-line (script) interface to instapy"""

import argparse
import sys

import numpy as np
from PIL import Image
from instapy.numpy_filters import numpy_color2gray, numpy_color2sepia
from instapy.python_filters import python_color2gray, python_color2sepia
from instapy.numba_filters import numba_color2gray, numba_color2sepia
from instapy.timing import time_one

from . import io

def run_filter(
    file: str,
    out_file: str = None,
    implementation: str = "python",
    filter: str = "color2gray",
    scale: int = 1,
    runtime: str = None
) -> None:
    """Run the selected filter"""
    # load the image from a file
    image =  (Image.open(file))
    
    if scale != 1:
        image = image.resize((image.width // int (scale), image.height // int (scale)))
        
    # Apply the filter
    image = np.asarray(image)
    avgtime = "Average time over 3 runs: "
    filtered = ...
    if filter.__eq__("gray") and implementation.__eq__("python"):
        filtered = python_color2gray(image)
        if runtime:
            print(avgtime, time_one(python_color2gray, image), "s")
            
    elif filter.__eq__("gray") and implementation.__eq__("numpy"):
        filtered = python_color2gray(image)
        if runtime:
            print(avgtime, time_one(numpy_color2gray, image), "s")          

    elif filter.__eq__("gray") and implementation.__eq__("numba"):
        filtered = numba_color2gray(image)
        if runtime:
            print(avgtime, time_one(numba_color2gray, image), "s")
        
    elif filter.__eq__("sepia") and implementation.__eq__("python"):
        filtered = python_color2sepia(image)
        if runtime:
            print(avgtime, time_one(python_color2sepia, image), "s")
             
    elif filter.__eq__("sepia") and implementation.__eq__("numpy"):
        filtered = numpy_color2sepia(image)
        if runtime:
            print(avgtime, time_one(numpy_color2sepia, image), "s")  
        
    elif filter.__eq__("sepia") and implementation.__eq__("numba"):
        filtered = numba_color2sepia(image)
        if runtime:
            print(avgtime, time_one(numba_color2sepia, image), "s")
            
    
    filtered = filtered.astype("uint8")
    if out_file:
        outimage= Image.fromarray(filtered)
        outimage.save(out_file)

    else:
        # not asked to save, display it instead
        io.display(filtered)


def main(argv=None):
    """Parse the command-line and call run_filter with the arguments"""
    if argv is None:
        argv = sys.argv[1:]

    parser = argparse.ArgumentParser()

    # filename is positional and required
    parser.add_argument("file", metavar = "FILE", help="The filename to apply filter to")
    parser.add_argument("-o", "--out", metavar ="OUT", help="The output filename", dest = "outfile")

    # Add required arguments
    parser.add_argument("-g", "--gray", help="Select gray filter", nargs='?', const = "gray", dest = "filter")
    parser.add_argument("-se","--sepia", help="Select sepia filter", nargs='?', const = "sepia", dest = "filter")
    parser.add_argument("-sc", "--scale", metavar = "SCALE", help= "Scale factor to resize image", default = 1, dest = "scale")
    parser.add_argument("-i", "--implemenation",choices=["python","numba","numpy"], help="The implementation", dest = "implementation")
    parser.add_argument("-r", "--runtime", help="Outputs the average runtime over 3 runs", action = "store_true")

    # parse arguments and call run_filter
    args = parser.parse_args()

    run_filter(args.file, args.outfile, args.implementation, args.filter, args.scale, args.runtime )

