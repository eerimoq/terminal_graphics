import numpy

from . import ctext
from .terminal import get_size


def write(image, fout, size=None):
    if size is None:
        terminal_size = get_size()

        if terminal_size.cell_pixels is None:
            raise Exception('Cannot show image with unknown dimensions.')

        size = (image.width // terminal_size.cell_pixels[0],
                image.height // terminal_size.cell_pixels[1])

    image = image.resize((size[0], 2 * size[1])).convert('RGB')
    ctext.write(image.height // 2, image.width, numpy.array(image))
