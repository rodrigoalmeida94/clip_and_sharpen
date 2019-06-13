"""
This is a sample processing block that always returns the input data.
"""
import json
import shutil
import rasterio
from rasterio.windows import Window


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
        window = Window(0, 0, 1000, 1000)
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
                                   

def run():
    clip_input()


def write_output(result):
    """
    Write the result data to the /tmp/output directory.

    If you are storing image data, you would need to then copy that data into this directory as well.
    """



if __name__ == "__main__":
    #data = load_input()
    #result = run(data)
    clip_input()
    #write_output(result)
