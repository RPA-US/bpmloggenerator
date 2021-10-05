from PIL import Image


def image_resolution(path):
    '''
    Detect the resolution of an image
    args:
        path: path of the image to be processed
    '''
    img = Image.open(path)
    width, height = img.size
    img.close()
    return width,height