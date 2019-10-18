from wand.image import Image
from wand.display import display
from wand.api import library

import os
import sys
import argparse


class Gifgud(object):

    def __init__(self):
        self.is_path = True

    def main(self):
        my_parser = argparse.ArgumentParser(prog='gifgud',
                                            description='Scales up gifs and whole folders of gifs')

        # Add the arguments
        my_parser.add_argument('input_path', metavar='input_path', type=str,
                               help='the path to folder containing gifs  or a gif')
        my_parser.add_argument('output_path', metavar='output_path', type=str,
                               help='the path to folder or file, where will be written to. ')
        my_parser.add_argument('-p', '--pixel', action='store', help='the output size in pixel (64x64)')
        my_parser.add_argument('-s', '--scale', action='store', help='scale of the output (2 = doubled size). '
                                                                          'Can only be used without -p --pixel '
                                                                          'the size in pixel')

        args = my_parser.parse_args()

        input_path = args.input_path
        output_path = args.output_path
        # pixel = args.

        if not os.path.isdir(input_path):
            self.is_path = False
            if not os.path.isfile(input_path):
                print('The path is not a directory or file')
                sys.exit()

        if self.is_path == False:
            self._scale_up(input_path, output_path)

    def _scale_up(self, file_path, output_path):
        with Image(filename=file_path) as img:
            print('width before =', img.width)
            print('height before =', img.height)
            # display(img)

            img.coalesce()
            # display(img)

            img.resize(1024, 1024)

            print('width after =', img.width)
            print('height after =', img.height)
            # display(img)

            img.save(filename=output_path)







if __name__ == "__main__":
    gg = Gifgud()
    gg.main()
