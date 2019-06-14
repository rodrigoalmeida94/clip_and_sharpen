"""
Test unit for Clip and Sharpen
"""
import json
import shutil
import time
import os
import rasterio
from rasterio.windows import Window
import numpy as np
from scipy import ndimage
import unittest
from run import *

class TestClipSharpen(unittest.TestCase):

    def test_high_pass_filter(self):
        test_array = np.zeros((3,3))
        self.assertEqual(high_pass_filter(test_array).size, 9)
        self.assertEqual(high_pass_filter(test_array), test_array)

if __name__ == '__main__':
    unittest.main()