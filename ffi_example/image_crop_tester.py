import os
import time
import logging
from PIL import Image

import sys
import ctypes
from ctypes import c_char_p
from ctypes import c_uint32

logger = logging.getLogger(__file__)


# load Rust
lib_name = 'crop'
prefix = {'win32': ''}.get(sys.platform, 'lib')
extension = {'darwin': '.dylib', 'win32': '.dll'}.get(sys.platform, '.so')
rust_ffi_lib = ctypes.cdll.LoadLibrary(prefix + lib_name + extension)

# identify the interface
rust_ffi_lib.crop_image.argtypes = (c_char_p, c_char_p, c_uint32, c_uint32, c_uint32, c_uint32)
rust_ffi_lib.crop_image.restype = c_uint32


def rust_crop_multiple_images(input_image_list, input_crop_area):
    """
    Crop image by Rust library
    """
    if input_crop_area['width'] % 2:
        input_crop_area['width'] -= 1
    if input_crop_area['height'] % 2:
        input_crop_area['height'] -= 1

    x = input_crop_area['x']
    y = input_crop_area['y']
    width = input_crop_area['width']
    height = input_crop_area['height']

    for input_image_data in input_image_list:
        try:
            if os.path.exists(input_image_data['output_fp']):
                # logger.debug("crop file[%s] already exists, skip crop actions!" % input_image_data['output_fp'])
                continue
            else:
                if os.path.isfile(input_image_data['input_fp']):

                    rust_ffi_lib.crop_image(input_image_data['input_fp'],
                                            input_image_data['output_fp'],
                                            x, y, width, height)
                else:
                    logger.warning("Incorrect image format of file during crop images: [%s]" % input_image_data['input_fp'])
                    continue
        except Exception as e:
            logger.error(e)


##################################################
# This method comes from lib/common/imageUtil.py #
##################################################
def crop_multiple_images(input_image_list, input_crop_area):
    """

    @param input_image_list:
    @param input_crop_area:
    @return:
    """
    if input_crop_area['width'] % 2:
        input_crop_area['width'] -= 1
    if input_crop_area['height'] % 2:
        input_crop_area['height'] -= 1
    crop_region = [input_crop_area['x'], input_crop_area['y'],
                   input_crop_area['x'] + input_crop_area['width'],
                   input_crop_area['y'] + input_crop_area['height']]
    for input_image_data in input_image_list:
        try:
            if os.path.exists(input_image_data['output_fp']):
                # logger.debug("crop file[%s] already exists, skip crop actions!" % input_image_data['output_fp'])
                continue
            else:
                if os.path.isfile(input_image_data['input_fp']):
                    # logger.debug("Crop file [%s] with crop area [%s]" % (input_image_data['input_fp'], crop_region))
                    src_img = Image.open(input_image_data['input_fp'])
                    dst_img = src_img.crop(crop_region)
                    dst_img.save(input_image_data['output_fp'])
                else:
                    logger.warning("Incorrect image format of file during crop images: [%s]" % input_image_data['input_fp'])
                    continue
        except Exception as e:
            logger.error(e)


# entry point
if __name__ == '__main__':
    # init logger
    default_log_format = '%(asctime)s %(levelname)s [%(name)s.%(funcName)s] %(message)s'
    default_datefmt = '%Y-%m-%d %H:%M'
    logging.basicConfig(level=logging.INFO, format=default_log_format, datefmt=default_datefmt)

    # define the const
    input_filename = 'Kings_College_London_Chapel_2.jpg'
    output_number = 10
    crop_area = {
        'x': 3050,
        'y': 2190,
        'width': 900,
        'height': 600
    }

    print('### Crop Image {} times ###'.format(output_number))

    # Rust FFI part
    rust_image_file_list = [
        {
            'input_fp': input_filename,
            'output_fp': 'rust_output_{}.jpg'.format(i)} for i in range(0, output_number)
    ]
    s_time = time.time()
    rust_crop_multiple_images(rust_image_file_list, crop_area)
    e_time = time.time()
    print('###   Rust: {} seconds ###'.format(e_time - s_time))

    # Python part
    py_image_file_list = [
        {
            'input_fp': input_filename,
            'output_fp': 'py_output_{}.jpg'.format(i)} for i in range(0, output_number)
    ]
    s_time = time.time()
    crop_multiple_images(py_image_file_list, crop_area)
    e_time = time.time()
    print('### Python: {} seconds ###'.format(e_time - s_time))
