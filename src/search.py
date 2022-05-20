import streamlit as st
import storage
from PIL import Image
from utils import resize_img_to_height, resize_img_to_width


def text_search() -> str:
    st.markdown("## Text Search")
    filename = st.text_input("Enter filename of image you want to find:")
    retrieved_filename = None 
    
    if filename:
        if not storage.image_exists(filename):
            st.error(f"{filename} does not exist in the repository!")
        else:
            img = storage.get_image(filename)
            st.image(img, caption=filename)
            retrieved_filename = filename
        
    return retrieved_filename




