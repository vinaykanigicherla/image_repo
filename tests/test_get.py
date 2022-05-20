import numpy as np 
from src import storage
from tests.utils import load_image, clean 
from PIL import Image

@clean
def test_image_get():
    img = load_image("dog1.jpg")
    storage.put_image(img, "dog1.jpg")
    assert isinstance(storage.get_image("dog1.jpg"), Image.Image)

@clean 
def test_vector_get():
    img = load_image("dog2.jpg")
    storage.put_image(img, "dog2.jpg")
    vec = storage.get_image_vector("dog2.jpg")
    assert isinstance(vec, np.ndarray)
    assert vec.shape == (1, 2048)

@clean
def test_nonexistent():
    assert storage.get_image("nonexistent.jpg") == None 
    assert storage.get_image_vector("nonexistent.jpg") == None 

@clean 
def test_multiple_gets():
    fns = ["dog1", "tiger1", "zebra1", "dog2", "tiger2", "zebra2"]
    image_keys = [fn+".jpg" for fn in fns]
    imgs = [load_image(ik) for ik in image_keys]

    storage.put_images(imgs, image_keys)

    for ik in image_keys:
        assert isinstance(storage.get_image(ik), Image.Image)
        assert storage.get_image_vector(ik).shape == (1, 2048)
    
    
