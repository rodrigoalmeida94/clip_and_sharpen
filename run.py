"""
This is a sample processing block that clips the input image to a given extent and sharpens the image.
"""
import json
import shutil
import time
import os
import rasterio
from rasterio.windows import Window
import numpy as np
from scipy import ndimage
import logging
logging.basicConfig(level=logging.INFO)

def load_input():
    """
    Load the input image from the filesystem
    """

    input_file = os.listdir('/tmp/input')
    if len(input_file) > 1:
        raise(ValueError, "More than 1 input file.")
    logging.info('Loading %s' % input_file[0])
    return '/tmp/input/'+input_file[0]

def clip_input(input_path, output_path='cropped.tif'):
    """
    Clip a chip of image
    :param str input_path: Path of input full image
    :param str output_path: Path of output clipped image
    """

    with rasterio.open(input_path, 'r') as img:
        logging.info('Clipping %s' % input_path)
        window = Window(1000, 1000, 250, 250)
        kwargs = img.meta.copy()
        kwargs.update({
        'driver':'GTiff',
            'height': window.height,
            'width': window.width,
            'transform': img.window_transform(window)})
        with rasterio.open(output_path, 'w', **kwargs) as out:
                out.write(img.read(window=window,
                                   out_shape=(img.count, window.height, window.width)))
        logging.info('Writting clipped image to %s' % input_path)
        return output_path

def high_pass_filter(data):
    """
    Apply high pass gaussian filter to np array
    :param np.array data: 2d array to apply filter
    """

    blurred = ndimage.gaussian_filter(data, 3)
    filter_blurred = ndimage.gaussian_filter(data, 1)
    sharpened = data + (data - filter_blurred)
    return sharpened

def run_high_pass(input_path, output_path='high_pass.tif'):
    """
    Run sharpen filter to image
    :param str input_path: Path of input image
    :param str output_path: Path of output sharpened image
    """

    with rasterio.open(input_path) as cropped:
        logging.info('Applying sharpening to %s' % input_path)
        kwargs = cropped.meta.copy()
        with rasterio.open(output_path, 'w', **kwargs) as out:
            out.write(high_pass_filter(cropped.read(1)), 1)
            out.write(high_pass_filter(cropped.read(2)), 2)
            out.write(high_pass_filter(cropped.read(3)), 3)
            out.write(high_pass_filter(cropped.read(4)), 4)
    logging.info('Writting sharpened image to %s' % output_path)
    return output_path

def run(data):
    """
    Run sharpen in image
    :param str data: Path of input image
    """
    output_path = run_high_pass(clip_input(data))
    return output_path

def write_output(result_path, output_file_name):
    """
    Write the result to tmp/output with a given name
    :param str result_path: Path of input image
    :param str output_file_name: File name to write to output folder
    """
    logging.info('Copying sharpened image to %s' % "/tmp/output/"+output_file_name)
    shutil.copy(result_path, "/tmp/output/"+output_file_name)

if __name__ == "__main__":
    start = time.time()
    data = load_input()
    result = run(data)
    write_output(result, "sharpened_"+os.path.splitext(os.path.basename(data))[0]+".tif")
    end = time.time()
    logging.info("Clip and Sharpen ran in %s s" % round(end - start, 2))
