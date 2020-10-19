from typing import List, Callable
import subprocess as sp
from multiprocessing import Process, Value


ConvertFunc = Callable[[str, str], sp.CompletedProcess]


class ParallelProcessor:
    @staticmethod
    def __check_success(input_file: str, output_file: str,
                        convert_func: ConvertFunc,
                        total_count: int,
                        success_count: Value, failure_count: Value) -> bool:
        """
        Check if conversion is successful.
        :param input_file: input file.
        :param output_file: output file.
        :param convert_func: conversion function.
        :param total_count: number of total conversions.
        :param success_count: synchronized success count.
        :param failure_count: synchronized failure count.
        :return: True if conversion is successful; False otherwise.
        """

        completed_process = convert_func(input_file, output_file)
        return_code = completed_process.returncode
        result = (return_code == 0)

        if result:
            success_count.value += 1
        else:
            failure_count.value += 1

        print(f'Success: {success_count.value} / {total_count}; '
              f'Failure: {failure_count.value} / {total_count}')
        return result

    @staticmethod
    def convert_all(input_files: List[str], output_files: List[str],
                    convert_func: ConvertFunc) -> None:
        """
        Run conversions in parallel.
        :param input_files: list of input files.
        :param output_files: list of output files.
        (Note: number of input and output files must match exactly.)
        :param convert_func: conversion function.
        :return: None.
        """

        num_conversions = len(input_files)
        assert num_conversions == len(output_files)

        all_processes: List[Process] = []
        success_count = Value('i', 0)
        failure_count = Value('i', 0)

        for (input_file, output_file) in zip(input_files, output_files):
            process = Process(
                target=ParallelProcessor.__check_success,
                args=(input_file, output_file, convert_func,
                      num_conversions, success_count, failure_count)
            )
            all_processes.append(process)

        for process in all_processes:
            process.start()

        for process in all_processes:
            process.join()

        print(f'TOTAL SUCCESS: {success_count.value} / {num_conversions}')
        print(f'TOTAL FAILURE: {failure_count.value} / {num_conversions}')
