#! -*- coding: utf-8 -*-

import argparse
import os
import numpy as np

from quantize import mmcq
from general_util import imread, get_all_image_paths


def get_palette(filename, color_count=10, quality=10):
    default_hw = 200
    default_shape = (default_hw, default_hw)

    with imread(path=filename, shape= default_shape, dtype=np.uint8) as image:
        colors = []
        for x in range(0, default_hw):
            for y in range(0, default_hw, quality):
                r,g,b = image[x,y]
                if r < 250 and g < 250 and b < 250:
                    colors.append((r, g, b))

        c_map = mmcq(colors, color_count)
        yield c_map.palette


def get_dominant_color(color_count=5, quality=10,):
    with get_palette(color_count, quality,) as palette:
        return palette[0]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_dir", required=True, help="Path to folder containing images.")
    parser.add_argument("--output_dir", required=True, help="where to put output files.")
    parser.add_argument("--color_count", type=int, default=10, help="weight on L1 term for generator gradient")
    parser.add_argument("--quality", type=int, default=10, help="weight on GAN term for generator gradient")

    a = parser.parse_args()

    if not os.path.exists(a.input_dir):
        raise Exception("input_dir does not exist")

    input_paths = get_all_image_paths(a.input_dir)

    if len(input_paths) == 0:
        raise Exception("input_dir contains no image files")

    for input_path in input_paths:
        with get_palette(filename=input_path, color_count=a.color_count, quality=a.quality) as palette:
            print palette