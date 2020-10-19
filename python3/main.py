import sys
import argparse

from utils.FileConverter import FileConverter


def main():
    # parse arguments
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--input-dir', required=True)
    arg_parser.add_argument('--output-dir', required=True)
    args = arg_parser.parse_args(sys.argv[1:])

    # batch conversion
    file_converter = FileConverter(args.input_dir)
    file_converter.convert_all_to_png(args.output_dir)


if __name__ == '__main__':
    main()
