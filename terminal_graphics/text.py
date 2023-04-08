import numpy

from . import ctext
from .terminal import get_size


def write(image, fout, size=None):
    if size is None:
        terminal_size = get_size()
        width_cells = terminal_size.cells[0] - 2
        height_cells = terminal_size.cells[1] - 2
        pixels_per_cell = max(image.width // width_cells,
                              image.height // (2 * height_cells))
        size = (min(width_cells, image.width // pixels_per_cell),
                min(height_cells, image.height // (2 * pixels_per_cell)))

    image = image.resize((size[0], 2 * size[1])).convert('RGB')
    ctext.write(image.height // 2, image.width, numpy.array(image))
