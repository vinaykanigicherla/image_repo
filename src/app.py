import streamlit as st
import argparse

import add_delete_images
import search

from PIL import Image 



def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--num_uploads_allowed", type=int, default=8, 
                        help="No. image uploads allowed at once per user")
    parser.add_argument("--img_preview_height", type=int, default=150, 
                        help="Height of image previews")


    args = parser.parse_args()
    NUM_UPLOADS_ALLOWED = args.num_uploads_allowed
    IMG_PREVIEW_HEIGHT = args.img_preview_height
    
    st.set_page_config(
     page_title="Image Repository!",
     page_icon="📸",
     layout="centered",
     initial_sidebar_state="auto",
 )

    st.sidebar.title("Image Repository")
    
    page = st.sidebar.selectbox("What do you want to do?", options=["View", "Add", "Search"])

    if page == "View":
        add_delete_images.display_images_section()
        add_delete_images.delete_all_section()
    if page == "Add":
        add_delete_images.file_uploader_section(NUM_UPLOADS_ALLOWED, IMG_PREVIEW_HEIGHT)
    if page == "Search":
        retrieved_filename = search.text_search()
        add_delete_images.delete_image_section(retrieved_filename)
    

if __name__ == "__main__":
    main()