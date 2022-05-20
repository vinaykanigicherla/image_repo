
from PIL import Image

def is_image_file(filename: str):
    return filename.split(".")[1] in {"png", "jpg"}


def resize_img_to_height(img: Image.Image, height: int) -> Image.Image:
    return img.resize((int(img.width * height/img.height), height))

def resize_img_to_width(img: Image.Image, width: int) -> Image.Image:
    return img.resize((width, int(img.height * width/img.width)))
