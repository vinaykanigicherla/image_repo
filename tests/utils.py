import os 
from PIL import Image  
from src.backend import storage

def load_image(filename: str) -> Image.Image:
    path = os.path.join("tests", "test_images", filename)
    img = Image.open(path)
    return img 

def _clean():
    failed_deletions = storage.delete_all_images()
    assert failed_deletions == []
    
def clean(func):
    def cleaned_func():
        _clean()
        func()
        _clean()
    return cleaned_func