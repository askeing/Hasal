import os
import cv2
import numpy


class DctRunTimeGenerator(object):
    def __init__(self, input_data, output_data):
        self.input_data = input_data
        self.output_data = output_data
        self.sample_data = {}
        for sample_fn in os.listdir(self.input_data['sample_dp']):
            sample_fp = os.path.join(self.input_data['sample_dp'], sample_fn)
            self.sample_data[sample_fp] = {'dct': self.convert_to_dct(sample_fp)}

    def compare_dct(self, dct_obj_1, dct_obj_2, threshold=0.0003):
        match = False
        try:
            row1, cols1 = dct_obj_1.shape
            row2, cols2 = dct_obj_2.shape
            if (row1 == row2) and (cols1 == cols2):
                mismatch_rate = numpy.sum(numpy.absolute(numpy.subtract(dct_obj_1, dct_obj_2))) / (row1 * cols1)
                if mismatch_rate <= threshold:
                    match = True
        except Exception as e:
            print e
        return match

    def gen_data(self, input_fp):
        dct_value = self.convert_to_dct(input_fp)
        for sample_fp in self.sample_data:
            if self.compare_dct(dct_value, self.sample_data[sample_fp]['dct']):
                print "%s = %s" % (input_fp, sample_fp)
                return sample_fp

    def convert_to_dct(self, image_fp, skip_status_bar_fraction=1.0):
        dct_obj = None
        try:
            img_obj = cv2.imread(image_fp)
            height, width, channel = img_obj.shape
            height = int(height * skip_status_bar_fraction) - int(height * skip_status_bar_fraction) % 2
            img_obj = img_obj[:height][:][:]
            img_gray = numpy.zeros((height, width))
            for channel in range(channel):
                img_gray += img_obj[:, :, channel]
            img_gray /= channel
            img_dct = img_gray / 255.0
            dct_obj = cv2.dct(img_dct)
        except Exception as e:
            print e
        return dct_obj

    def gen_result(self):
        pass

