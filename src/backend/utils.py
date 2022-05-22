import streamlit as st
from PIL import Image
from typing import Dict

def is_image_file(filename: str):
    """Tell whether a filename corresponds to an image file"""
    return filename.split(".")[1] in {"png", "jpg"}

def resize_img_to_height(img: Image.Image, height: int) -> Image.Image:
    """Resize image to certain height while maintaining aspect ratio"""
    return img.resize((int(img.width * height/img.height), height))

def resize_img_to_width(img: Image.Image, width: int) -> Image.Image:
    """Resize image to certain width while maintaining aspect ratio"""
    return img.resize((width, int(img.height * width/img.width)))

def image_gallery(fn_to_img: Dict[str, Image.Image]):
    """Display multiple images in two columns arranged such that column heights are approx equal"""  
    display_original_size = st.checkbox("Display images in original size?")
    
    if not display_original_size:
        resize_width = st.number_input("Enter desired image width (in pixels):", min_value=100, max_value=500) 
    else:
        resize_width = None

    cols = st.columns(2)
    col_heights = [0, 0]
    for fn, _img in fn_to_img.items():
        curr_col = 0 if col_heights[0] <= col_heights[1] else 1
        img = _img if resize_width == None else resize_img_to_width(_img, resize_width)
        cols[curr_col].image(img, caption=fn)
        col_heights[curr_col] += img.height
