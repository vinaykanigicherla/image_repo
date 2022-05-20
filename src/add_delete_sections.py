import streamlit as st

import storage

from PIL import Image

from utils import resize_img_to_height, image_gallery

def file_uploader_section(num_uploads_allowed: int, img_display_height: int):
    """Section to upload images and add to repository"""
    st.markdown("## Add Images:")
    uploads = []
    uploads = st.file_uploader("Upload Image(s):", type = ["png", "jpg"], accept_multiple_files = True)
    uploads = uploads if isinstance(uploads, list) else [uploads] 
    filenames = [u.name for u in uploads]

    if len(uploads) > num_uploads_allowed:
        st.error(f"You cannot upload more than {num_uploads_allowed} files at once!")
        st.stop()

    if len(uploads) > 0:
        imgs = [Image.open(u) for u in uploads]
        st.image([resize_img_to_height(img, img_display_height) for img in imgs[:num_uploads_allowed]])
        
        upload_button = st.button(f"Upload {len(imgs)} images")
        
        if upload_button:
            with st.spinner("Uploading..."):
                failed_uploads = storage.put_images(imgs, filenames)

            if len(failed_uploads) == 0:
                st.success("Successfully uploaded images! Refresh to view changes.")
            else:
                st.error(f"The following files failed to upload, please try again: {failed_uploads}")


def display_images_section():
    """Section for displaying images stored in the repository"""
    st.markdown("## Stored Images:")
    order_by_option = st.selectbox("Attribute to order by:", options=["Date Added", "Size", "Filename"])
    

    display_all = st.checkbox("Display all images?")
    if not display_all:
        num_imgs_to_display = st.number_input("Number of images to display:", min_value=0)
    else:
        num_imgs_to_display = None 

    with st.spinner("Fetching images..."):
        fn_to_img = storage.get_images(num_imgs_to_display, order_by_option)
    
    if len(fn_to_img) == 0:
        st.markdown("### -- Nothing to display! --")
        st.stop()
    else:
        image_gallery(fn_to_img)


def delete_image_section(filename: str):
    """Section to delete an image named filename"""
    if filename:
        if st.button(f"Delete {filename}?"):
            if storage.delete_image(filename):
                st.success(f"Deleted {filename}! Refresh to view changes.")
            else:
                st.error("Could not complete deletion.")


def delete_all_section() -> bool:
    """Section to clear image repository"""
    if "delete_all" not in st.session_state:
        st.session_state["delete_all"] = False 

    if st.button("Clear Database"):
        st.session_state["delete_all"] = True 

    if st.session_state["delete_all"]:
        confirmation = st.text_input("Please type 'Clear Database' to confirm your intent:")
        if confirmation:
            if confirmation != "Clear Database":
                st.error("Incorrect input! Please try again!")
            else:
                st.session_state["delete_all"] = False 
                with st.spinner("Deleting..."):
                    failed_deletions = storage.delete_all_images()
                if not failed_deletions:
                    st.success("Cleared all images in database! Please refresh to view changes.")
                else:
                    st.error(f"Was able to delete all images except the following: {failed_deletions}")



