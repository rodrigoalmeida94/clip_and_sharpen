"""
This is a sample processing block that clips the input image to a given extent and sharpens the image.
"""
import json
import shutil
import os
import rasterio
from rasterio.windows import Window
import numpy as np
from scipy import ndimage


IMGFILE = "data/FCGC600031063/IMG_PHR1A_MS_002/IMG_PHR1A_MS_201202250025599_ORT_PRG_FC_5852-002_R1C1.JP2"


def load_input():
    """
    Load the input image from the filesystem
    """
    input_file = os.listdir('/tmp/input')
    if len(input_file) > 1:
        raise(ValueError, "More than 1 input file.")
    return '/tmp/input/'+input_file[0]

def clip_input(input_path, output_path='cropped.tif'):
    """
    Clip a chip of image
    :img: rasterio dataset
    """

    with rasterio.open(input_path, 'r') as img:
        window = Window(1000, 1000, 250, 250)
        kwargs = img.meta.copy()
        kwargs.update({
        'driver':'GTiff',
            'height': window.height,
            'width': window.width,
            'transform': img.window_transform(window)})
        print(kwargs)
        with rasterio.open(output_path, 'w', **kwargs) as out:
                out.write(img.read(window=window,
                                   out_shape=(img.count, window.height, window.width)))
        return output_path

def high_pass_filter(data):
    blurred = ndimage.gaussian_filter(data, 3)
    filter_blurred = ndimage.gaussian_filter(data, 1)
    sharpened = data + (data - filter_blurred)
    return sharpened

def run_high_pass(input_path, output_path='high_pass.tif'):
    with rasterio.open(input_path) as cropped:
        kwargs = cropped.meta.copy()
        with rasterio.open(output_path, 'w', **kwargs) as out:
            out.write(high_pass_filter(cropped.read(1)), 1)
            out.write(high_pass_filter(cropped.read(2)), 2)
            out.write(high_pass_filter(cropped.read(3)), 3)
            out.write(high_pass_filter(cropped.read(4)), 4)
    return output_path

def run(data):
    output_path = run_high_pass(clip_input(data))
    return output_path


def write_output(result_path, output_file_name):
    """
    Write the result data to the /tmp/output directory.

    If you are storing image data, you would need to then copy that data into this directory as well.
    """
    shutil.copy(result_path, "/tmp/output/"+output_file_name)



if __name__ == "__main__":
    data = load_input()
    result = run(data)
    write_output(result, "sharpened_"+os.path.basename(data))
