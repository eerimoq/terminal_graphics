from PIL.ImageOps import pad
from dataclasses import dataclass


@dataclass
class Size:
    width: int
    height: int


def split_image_horizontally(image, number_of_images):
    """Split given image horizontally into given number of images.

    """

    height = (image.height + number_of_images - 1) // number_of_images

    for y in range(0, image.height, height):
        yield image.crop((0, y, image.width, y + height))


def pad_ratio(image, size, cell_size=None):
    """Pad to fit given size. Keeps aspect ratio.

    """

    if cell_size is None:
        cell_size = Size(1, 2)

    image_ratio = image.width / image.height
    size_ratio = (size.width * cell_size.width) / (size.height * cell_size.height)

    if image_ratio < size_ratio:
        width = int(image.height * size_ratio)
        height = image.height
    else:
        width = image.width
        height = int(image.width / size_ratio)

    return pad(image, (width, height))
