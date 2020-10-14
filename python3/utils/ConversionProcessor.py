from typing import List
import glob
from os.path import abspath, join, basename, splitext
import subprocess as sp
from multiprocessing import Process


class ConversionProcessor:

    convert_exec = 'opj_decompress'

    def __init__(self, input_dir: str):
        self.__jp2_images = self.__get_jp2_files(input_dir)
        self.__jpg_jpeg_images = self.__get_jpg_jpeg_files(input_dir)

    @staticmethod
    def get_files_by_ext(input_dir: str, ext: str) -> List[str]:
        """
        Get the collection of input files, by specified extension.
        :param input_dir: Input directory.
        :param ext: File extension. MUST START WITH '.'
        :return: The list of files with specified extension (absolute paths)
        """
        input_files = glob.glob(join(input_dir, f'**/*{ext}'),
                                recursive=True)
        input_files = list(map(abspath, input_files))
        input_files.sort()
        return input_files

    def __get_jp2_files(self, input_dir: str) -> List[str]:
        """
        Get the collection of jp2 files.
        :param input_dir: input directory.
        :return: the list of jp2 files.
        """
        self.__jp2_images = self.get_files_by_ext(input_dir, '.jp2')
        return self.__jp2_images

    def __get_jpg_jpeg_files(self, input_dir: str) -> List[str]:
        """
        Get the collection of jpg & jpeg files.
        :param input_dir: input directory.
        :return: the list of jpg & jpeg files.
        """
        self.__jpg_jpeg_images = self.get_files_by_ext(input_dir, '.jpg') + \
            self.get_files_by_ext(input_dir, '*.jpeg')
        return self.__jpg_jpeg_images

    @staticmethod
    def __convert_from_jpeg2000(input_file: str, output_file: str) -> int:
        """
        Read in a jpeg2000 image, and convert it to another image type.
        See "man opj_decompress.1" for more details.

        :param input_file: Path of input file.
            Valid input formats: .j2k, .jp2, .j2c, .jpt
        :param output_file: Path of output file.
            Valid output formats: .bmp, .pgm, .pgx, .png,  .pnm,  .ppm, .raw, .tga, .tif
        :return: the return code of completed process.
        """

        output_file = abspath(output_file)  # output absolute path in console
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
            process = Process(target=self.__convert_from_jpeg2000,
                              args=(jp2_image, output_file))
            all_processes.append(process)
            process.start()

        for process in all_processes:
            process.join()
