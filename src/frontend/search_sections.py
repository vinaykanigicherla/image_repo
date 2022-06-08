import streamlit as st
from backend import storage
from PIL import Image
from backend.utils import image_gallery, resize_img_to_height, resize_img_to_width


def text_search() -> str:
    """Section to search for an image by its filename"""
    st.markdown("## Text Search")
    filename = st.text_input("Enter filename of image you want to find:")
    retrieved_filename = None 
    
    if filename:
        if not storage.exists(filename):
            st.error(f"{filename} does not exist in the repository!")
        else:
            img = storage.get_image(filename)
            st.image(img, caption=filename)
            retrieved_filename = filename
        
    return retrieved_filename

def image_search() -> str:
    """Section to see images in the repository that are similar to an uploaded image"""
    st.markdown("## Reverse Image Search")
    
    upload = st.file_uploader("Upload Image to search for similar images in repository:", type = ["png", "jpg"])
    
    if upload:
        img = Image.open(upload)
        st.image(img)
    
    num_similar = st.number_input("How many of the most similar images do you want to see?", min_value=0, max_value=20)
    
    if upload and num_similar > 0:
        with st.spinner():
            image_gallery(storage.get_similar_imgs(img, num_similar))


def semantic_search() -> str:
    """Section to see images in the repository that are similar to a query text"""
    st.markdown("## Semantic Search")
    
    text = st.text_input("Enter query text:")
    
    
    num_similar = st.number_input("How many of the relevant images do you want to see?", min_value=0, max_value=20)
    
    if text and num_similar > 0:
        with st.spinner():
            image_gallery(storage.get_similar_imgs_text(text, num_similar))


