def split_image_horizontally(image, number_of_images):
    """Split given image horizontally into given number of images.

    """

    height = (image.height + number_of_images - 1) // number_of_images

    for y in range(0, image.height, height):
        yield image.crop((0, y, image.width, y + height))
