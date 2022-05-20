from PIL import Image 
from os.path import join 
from src.storage import delete_all_images

def load_image(filename: str) -> Image.Image:
    path = join("test_images", filename)
    img = Image.open(path)
    return img 

def _clean():
    failed_deletions = delete_all_images()
    assert failed_deletions == []
    
def clean(func):
    def cleaned_func():
        _clean()
        func()
        _clean()
    return cleaned_func