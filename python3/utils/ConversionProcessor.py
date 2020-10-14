from typing import List
import glob
from os.path import abspath, join, basename, splitext
import subprocess as sp
from multiprocessing import Process


class ConversionProcessor:

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
    def __convert_from_jpeg2000(input_img: str, output_img: str) -> int:
        """
        Read in a jpeg2000 image, and convert it to another image type.
        See "man opj_decompress.1" for more details.

        :param input_img: Path of input image.
            Valid input formats: .j2k, .jp2, .j2c, .jpt
        :param output_img: Path of output image.
            Valid output formats: .bmp, .pgm, .pgx, .png,  .pnm,  .ppm, .raw, .tga, .tif
        :return: the return code of completed process.
        """
        convert_exec = 'opj_decompress'
        output_img = abspath(output_img)  # output absolute path in console
        return sp.run([convert_exec, '-i', input_img,
                       '-o', output_img]).returncode

    @staticmethod
    def __convert_jpg_jpeg_to_png(input_img: str, output_img: str) -> int:
        """
        Convert from jpg / jpeg to png.
        See "man convert.1" for more details.
        :param input_img: Path of input image.
        :param output_img: Path of output image.
        :return: the return code of completed process.
        """
        convert_exec = 'convert-im6.q16'
        return sp.run([convert_exec, '-verbose',
                       input_img, output_img]).returncode

    @staticmethod
    def convert_to_png(input_img: str, output_img: str) -> int:
        """
        Convert input image to png.
        :param input_img: Path of input image.
        :param output_img: Path of output image.
            If output extension is not .png, it will be corrected automatically.
        :return: Return code for conversion.
        """

        jpeg2000_exts = ['.j2k', '.jp2', '.j2c', '.jpt']
        input_ext = splitext(input_img)[1]
        output_img = f'{splitext(output_img)[0]}.png'

        if input_ext in jpeg2000_exts:
            return ConversionProcessor.__convert_from_jpeg2000(input_img, output_img)
        else:
            return ConversionProcessor.__convert_jpg_jpeg_to_png(input_img, output_img)

    def convert_all(self, output_dir: str,
                    output_ext: str = '.png') -> None:
        """
        Convert all jp2 to output format (default is .png).
        :return: None.
        """

        all_processes: List[Process] = []

        for input_img in [*self.__jp2_images, *self.__jpg_jpeg_images]:
            output_img = join(output_dir, splitext(basename(input_img))[0])
            output_img = f'{output_img}{output_ext}'
            process = Process(target=self.convert_to_png,
                              args=(input_img, output_img))
            all_processes.append(process)
            process.start()

        for process in all_processes:
            process.join()
