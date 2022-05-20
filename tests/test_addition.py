from src import storage
from tests.utils import load_image, clean 


@clean
def test_empty():
    assert storage.num_images() == 0

@clean
def test_image_exists():
    img = load_image("dog1.jpg")
    storage.put_image(img, "dog1.jpg")
    assert storage.exists("dog1.jpg")

@clean 
def test_image_vector_exists():
    img = load_image("dog2.jpg")
    storage.put_image(img, "dog2.jpg")
    assert storage.exists("dog2.jpg") #image
    assert storage.exists("dog2.npy") #image vector
    
@clean 
def test_multiple_images():
    fns = ["dog1", "tiger1", "zebra1", "dog2", "tiger2", "zebra2"]
    image_keys = [fn+".jpg" for fn in fns]
    vector_keys = [fn+".npy" for fn in fns]
    imgs = [load_image(ik) for ik in image_keys]

    failed_uploads = storage.put_images(imgs, image_keys)
    assert failed_uploads == []
    assert storage.num_images() == len(fns)

    for ik, vk in zip(image_keys, vector_keys):
        assert storage.exists(ik)
        assert storage.exists(vk)
    
    
