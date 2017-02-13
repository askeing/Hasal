import os
import shutil
import subprocess


class FfmpegConverter(object):

    def __init__(self, input_video_fp, output_img_dp, input_converting_fmt="bmp"):
        self.input_video_fp = input_video_fp
        self.output_img_dp = output_img_dp
        self.converting_fmt = input_converting_fmt

    def start_converting(self):
        if os.path.exists(self.output_img_dp):
            shutil.rmtree(self.output_img_dp)
        os.mkdir(self.output_img_dp)
        output_img_fmt = self.output_img_dp + os.sep + 'img%05d.' + self.converting_fmt.lower()
        cmd_list = ['ffmpeg', '-i', self.input_video_fp, output_img_fmt]
        ffmpeg_process = subprocess.Popen(cmd_list)
        return ffmpeg_process
