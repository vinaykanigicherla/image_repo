from src.backend import storage
from utils import load_image, clean 
from PIL import Image


@clean 
def test_image_search_1():
    fns = ["dog1", "duck1", "zebra1", "dog2", "duck2", "zebra2"]
    image_keys = [fn+".jpg" for fn in fns]
    imgs = [load_image(ik) for ik in image_keys]

    storage.put_images(imgs, image_keys)

    similar_imgs = storage.get_similar_imgs(load_image("dog3.jpg"), 2)
    assert "dog1.jpg" in similar_imgs
    assert "dog2.jpg" in similar_imgs

@clean 
def test_image_search_2():
    fns = ["dog1", "duck1", "zebra1", "dog2", "duck2", "zebra2"]
    image_keys = [fn+".jpg" for fn in fns]
    imgs = [load_image(ik) for ik in image_keys]

    storage.put_images(imgs, image_keys)

    similar_imgs = storage.get_similar_imgs(load_image("zebra3.jpg"), 2)
    assert "zebra1.jpg" in similar_imgs
    assert "zebra2.jpg" in similar_imgs
   
@clean 
def test_image_search_3():
    fns = ["dog1", "duck1", "zebra1", "dog2", "duck2", "zebra2"]
    image_keys = [fn+".jpg" for fn in fns]
    imgs = [load_image(ik) for ik in image_keys]

    storage.put_images(imgs, image_keys)

    similar_imgs = storage.get_similar_imgs(load_image("duck3.jpg"), 2)
    assert "duck1.jpg" in similar_imgs
    assert "duck2.jpg" in similar_imgs

    
