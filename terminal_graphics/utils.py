from PIL.ImageOps import pad


def split_image_horizontally(image, number_of_images):
    """Split given image horizontally into given number of images.

    """

    height = (image.height + number_of_images - 1) // number_of_images

    for y in range(0, image.height, height):
        yield image.crop((0, y, image.width, y + height))


def pad_ratio(image, size):
    """Pad to fit given size. Keeps aspect ratio.

    """

    image_ratio = image.width / image.height
    size_ratio = size[0] / size[1] / 2

    if image_ratio < size_ratio:
        width = int(image.height * size_ratio)
        height = image.height
    else:
        width = image.width
        height = int(image.width / size_ratio)

    return pad(image, (width, height))
