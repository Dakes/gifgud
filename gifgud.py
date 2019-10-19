from wand.image import Image
from wand.display import display
from wand.api import library

import os
import sys
import argparse


class Gifgud(object):

    def main(self):
        my_parser = argparse.ArgumentParser(prog='gifgud',
                                            description='Scales up gifs and whole folders of gifs')

        # Add the arguments
        my_parser.add_argument('input_path', metavar='input_path', type=str,
                               help='the path to a file, or folder containing gifs or other images')
        my_parser.add_argument('output_path', metavar='output_path', type=str,
                               help='the path to folder or file, where will be written to. ')
        my_parser.add_argument('-p', '--pixel', action='store', dest='pixel', help='the output pixel size (64x64)')
        my_parser.add_argument('-s', '--scale', action='store', dest='scale',
                               help='scale of the output (2 = doubled size). Can only be used without -p --pixel. '
                                    'The default is 2x')

        args = my_parser.parse_args()

        input_path = args.input_path
        output_path = args.output_path

        if not os.path.isdir(input_path):
            if not os.path.isfile(input_path):
                print('The path is not a directory or file')
                sys.exit(1)

        # single file convert
        if not os.path.isdir(input_path):
            with Image(filename=input_path) as img:
                img = self._scale_up(img, args.pixel, args.scale)
                img.save(filename=output_path)

        # recursive convert
        elif os.path.isdir(input_path):
            try:
                os.mkdir(output_path)
            except FileExistsError:
                pass
            for root, d_names, f_names in os.walk(input_path):
                for file_name in f_names:
                    file_path = os.path.join(root, file_name)
                    relative_path = os.path.relpath(file_path, input_path)
                    output_file = os.path.join(output_path, relative_path)

                    out_folder = os.path.dirname(output_file)
                    try:
                        os.mkdir(out_folder)
                    except FileExistsError:
                        pass

                    # print("Current Image: ", file_path)
                    try:
                        with Image(filename=file_path) as img:
                            img = self._scale_up(img, args.pixel, args.scale)
                            img.save(filename=output_file)
                    except Exception as err:
                        # print("found non image file: ", file_path)
                        pass

    def _scale_up(self, img, pixel, scale):
        """
        gets the new image size and scales the image up
        :param img:
        :param pixel:
        :param scale:
        :return: scaled up image
        """
        # TODO: Error checks and all that stuff
        if pixel:
            new_dimensions = pixel.lower().split("x")
            new_dimensions[0] = int(new_dimensions[0])
            new_dimensions[1] = int(new_dimensions[1])
        elif scale:
            scale = int(scale)
            new_dimensions = [img.width * scale, img.height * scale]
        else:
            new_dimensions = [img.width * 2, img.height * 2]

        img.coalesce()
        img.resize(new_dimensions[0], new_dimensions[1])
        return img


if __name__ == "__main__":
    gg = Gifgud()
    gg.main()
