from typing import List
import glob
from os.path import abspath, join, basename, splitext
import subprocess as sp
from multiprocessing import Process


class ConversionProcessor:

    convert_exec = 'opj_decompress'

    def __init__(self, input_dir: str):
        self.__jp2_images = self.get_jp2_files(input_dir)

    def get_jp2_files(self, input_dir: str):
        """
        Get the collection of jp2 files.
        :param input_dir: input directory.
        :return: the list of jp2 files.
        """
        jp2_files_list = glob.glob(join(input_dir, '**/*.jp2'),
                                   recursive=True)
        jp2_files_list = list(map(abspath, jp2_files_list))
        self.__jp2_images = jp2_files_list
        return jp2_files_list

    @staticmethod
    def convert(input_file: str, output_file: str) -> int:
        """
        Read in a jpeg2000 image, and convert to another format.
        Supported input formats: .j2k, .jp2, .j2c, .jpt
        Supported output formats: .bmp, .pgm, .pgx, .png,  .pnm,  .ppm, .raw, .tga, .tif
        See "man opj_decompress.1" for more details.

        :param input_file: Path of input file.
        :param output_file: Path of output file.
        :return: the return code of completed process.
        """

        return sp.run([ConversionProcessor.convert_exec, '-i', input_file,
                       '-o', output_file]).returncode

    def convert_all(self, output_dir: str,
                    output_ext: str = '.png') -> None:
        """
        Convert all jp2 to output format (default is .png).
        :return: None.
        """

        all_processes: List[Process] = []

        for jp2_image in self.__jp2_images:
            output_file = f'{join(output_dir, splitext(basename(jp2_image))[0])}{output_ext}'
            process = Process(target=self.convert, args=(jp2_image, output_file))
            all_processes.append(process)
            process.start()

        for process in all_processes:
            process.join()
