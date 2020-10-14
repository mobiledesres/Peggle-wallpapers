from utils.ConversionProcessor import ConversionProcessor


def main():
    conversion_processor = ConversionProcessor('../Peggle Nights Deluxe')
    conversion_processor.convert_all(output_dir='../Peggle Nights Deluxe/png')


if __name__ == '__main__':
    main()
