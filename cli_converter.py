import argparse
from argparse import ArgumentDefaultsHelpFormatter
import lib.calculator.parallelRunVideoCalculator as ParallelRunVideoCalculator


def main():
    arg_parser = argparse.ArgumentParser(description='Image tool',
                                         formatter_class=ArgumentDefaultsHelpFormatter)
    arg_parser.add_argument('-i', '--input', action='store', dest='input_video_fp', default=None,
                            help='Specify the file path.', required=False)
    arg_parser.add_argument('-o', '--outputdir', action='store', dest='output_img_dp', default=None,
                            help='Specify output image dir path.', required=False)
    arg_parser.add_argument('-s', '--sample', action='store', dest='sample_img_dp', default=None,
                            help='Specify sample image dir path.', required=False)
    args = arg_parser.parse_args()

    calculator_settings = {'converter': {'path': 'lib.converter.ffmpegConverter', 'name': 'FfmpegConverter'},
                            'generator': [{'path': 'lib.generator.dctRunTimeGenerator',
                                           'name': 'DctRunTimeGenerator',
                                           'deplib': ['cv2', 'numpy']}],
                            'settings': {'default_thread_no': 4, 'default_max_thread_no': 8,
                                         'default_sleep_time': 3}
                            }
    input_data = {'video_fp': args.input_video_fp, 'sample_dp': args.sample_img_dp}
    output_data = {'image_dp': args.output_img_dp}

    ParallelRunVideoCalculator.run(calculator_settings, input_data, output_data)

if __name__ == '__main__':
    main()
