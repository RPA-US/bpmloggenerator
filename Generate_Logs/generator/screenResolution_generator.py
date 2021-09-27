from PIL import Image

def image_resolution(path):
    img = Image.open(path)
    width, height = img.size
    img.close()
    return width,height