from src import storage
from tests.utils import load_image, clean 

@clean
def test_image_delete():
    img = load_image("dog1.jpg")
    storage.put_image(img, "dog1.jpg")
    assert storage.delete_image("dog1.jpg")
    assert not storage.exists("dog1.jpg")

@clean
def test_nonexistent_image_delete():
    assert not storage.exists("nonexistent.jpg")
    assert storage.delete_image("nonexistent.jpg") == False 


@clean 
def test_image_vector_delete():
    img = load_image("dog2.jpg")
    storage.put_image(img, "dog2.jpg")
    assert storage.delete_image(img, "dog2.jpg") == True 
    assert not storage.exists("dog2.jpg") #image
    assert not storage.exists("dog2.npy") #image vector
    
@clean 
def test_delete_all():
    fns = ["dog1", "tiger1", "zebra1", "dog2", "tiger2", "zebra2"]
    image_keys = [fn+".jpg" for fn in fns]
    vector_keys = [fn+".npy" for fn in fns]
    imgs = [load_image(ik) for ik in image_keys]

    storage.put_images(imgs, image_keys)
    failed_deletions = storage.delete_all_images()
    assert failed_deletions == []
    assert storage.num_images() == 0

    for ik, vk in zip(image_keys, vector_keys):
        assert not storage.exists(ik)
        assert not storage.exists(vk)
    
    
