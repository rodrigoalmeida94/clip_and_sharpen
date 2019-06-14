"""
This is a sample processing block that clips the input image to a given extent and sharpens the image.
"""
import json
import shutil
import rasterio
from rasterio.windows import Window
import numpy as np
from scipy import ndimage


IMGFILE = "data/FCGC600031063/IMG_PHR1A_MS_002/IMG_PHR1A_MS_201202250025599_ORT_PRG_FC_5852-002_R1C1.JP2"


def load_input():
    """
    Load the input image from the filesystem
    """
    return rasterio.open(IMGFILE)

def clip_input():
    """
    Clip 200 by 200 chip of image
    :img: rasterio dataset
    """

    with rasterio.open(IMGFILE, 'r') as img:
        window = Window(1000, 1000, 1000, 1000)
        kwargs = img.meta.copy()
        kwargs.update({
        'driver':'GTiff',
            'height': window.height,
            'width': window.width,
            'transform': img.window_transform(window)})
        print(kwargs)
        with rasterio.open('tmp/cropped.tif', 'w', **kwargs) as out:
                out.write(img.read(window=window,
                                   out_shape=(img.count, window.height, window.width)))

def high_pass_filter(data):
    blurred = ndimage.gaussian_filter(data, 3)
    filter_blurred = ndimage.gaussian_filter(data, 1)
    sharpened = data + (data - filter_blurred)
    return sharpened

def run_high_pass():
    with rasterio.open('tmp/cropped.tif') as cropped:
        kwargs = cropped.meta.copy()
        with rasterio.open('tmp/high_pass.tif', 'w', **kwargs) as out:
            out.write(high_pass_filter(cropped.read(1)), 1)
            out.write(high_pass_filter(cropped.read(2)), 2)
            out.write(high_pass_filter(cropped.read(3)), 3)
            out.write(high_pass_filter(cropped.read(4)), 4)

def run():
    clip_input()
    run_high_pass()


def write_output(result):
    """
    Write the result data to the /tmp/output directory.

    If you are storing image data, you would need to then copy that data into this directory as well.
    """



if __name__ == "__main__":
    #data = load_input()
    #result = run(data)
    #write_output(result)
    run()
