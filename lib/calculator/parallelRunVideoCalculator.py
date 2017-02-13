import pp
import os
import cv2
import numpy
import time
import copy
import importlib


def generate_chunks(input_list, input_chunk_no):
    return_list = []
    average_index = len(input_list) / float(input_chunk_no)
    last_index = 0.0
    while last_index < len(input_list):
        return_list.append(input_list[int(last_index):int(last_index + average_index)])
        last_index += average_index
    return return_list


def convert_to_dct(image_fp, skip_status_bar_fraction=1.0):
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

def parallel_compare_image(generator_obj_list, output_data, result_queue, input_chunk_list):
    result_data = {}
    # get start time of method
    for input_fn in input_chunk_list:
        input_fp = os.path.join(output_data['image_dp'], input_fn)
        #convert_to_dct(input_fp)
        for generator_obj in generator_obj_list:
            # get start time of gen_data
            result_sample_fp = generator_obj.gen_data(input_fp)
            if result_sample_fp:
                if result_sample_fp in result_data:
                    result_data[result_sample_fp].append(input_fp)
                else:
                    result_data[result_sample_fp] = [input_fp]
    return result_data
            # get end time of gen_data
            # print total time of gen_data
    # get end time of method
    # print total time of method


def parallel_generate_data(calculator_settings, generator_obj_list, generator_gen_data_fp_list, generator_deplib_list, input_data, output_data, current_fn_list):
    result_data = {}
    jobs = []
    # init ppservers
    ppservers = ()
    job_server = pp.Server(calculator_settings['settings']['default_thread_no'], ppservers=ppservers)

    # divide fn_list to thread_no portion
    chunk_list = generate_chunks(current_fn_list, calculator_settings['settings']['default_thread_no'])
    print "chunk number [%s]" % str(len(chunk_list))
    print "chunk 1 [%s]" % str(len(chunk_list[0]))
    print "chunk 2 [%s]" % str(len(chunk_list[1]))
    print "chunk 3 [%s]" % str(len(chunk_list[2]))
    print "chunk 4 [%s]" % str(len(chunk_list[3]))

    # parallel execute all generator's gen_raw_data function
    for index in range(len(chunk_list)):
        jobs.append(job_server.submit(parallel_compare_image, (generator_obj_list, output_data, None, chunk_list[index]),
                          (convert_to_dct,), tuple(generator_deplib_list)))

    for job in jobs:
        result_data.update(job())
    print result_data


def run(calculator_settings, input_data, output_data):
    # init converter object
    converter_class = getattr(importlib.import_module(calculator_settings['converter']['path']),
                              calculator_settings['converter']['name'])
    converter_obj = converter_class(input_data['video_fp'], output_data['image_dp'])

    # converting videos to images (default converter should be ffmpegconverter)
    converter_obj.start_converting()

    start_counter = 0
    processed_img_fn_list = []
    generator_result = {}

    # init generator object
    generator_obj_list = []
    generator_gen_data_fp_list = []
    generator_gen_result_fp_list = []
    generator_deplib_list = []
    for generator_data in calculator_settings['generator']:
        generator_class = getattr(importlib.import_module(generator_data['path']), generator_data['name'])
        generator_obj = generator_class(input_data, output_data)
        generator_obj_list.append(generator_obj)
        generator_gen_data_fp_list.append(generator_obj.gen_data)
        generator_gen_result_fp_list.append(generator_obj.gen_result)
        for deplib in generator_data['deplib']:
            if deplib not in generator_deplib_list:
                generator_deplib_list.append(deplib)


    time.sleep(calculator_settings['settings']['default_sleep_time'])
    while True:
        print "start_counter = [%s]" % str(start_counter)
        current_img_fn_list = os.listdir(output_data['image_dp'])
        if start_counter == len(current_img_fn_list):
            print "converting process is completed!"
            break
        else:
            # TODO: filter image list
            # TODO: crop image
            start_counter = len(current_img_fn_list)
            processing_img_fn_list = copy.deepcopy(list(set(current_img_fn_list) - set(processed_img_fn_list)))
            processing_img_fn_list.sort()
            print "processing_img_fn_list [%s] - [%s]" % (processing_img_fn_list[0], processing_img_fn_list[-1])
            parallel_generate_data(calculator_settings, generator_obj_list, generator_gen_data_fp_list, generator_deplib_list, input_data, output_data, processing_img_fn_list)
            processed_img_fn_list.extend(copy.deepcopy(processing_img_fn_list))
    return generator_result
