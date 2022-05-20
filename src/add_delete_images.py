import streamlit as st

import storage

from PIL import Image

from utils import resize_img_to_height, resize_img_to_width

def file_uploader_section(num_uploads_allowed: int, img_display_height: int):
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
            failed_uploads = storage.put_images(imgs, filenames)

            if len(failed_uploads) == 0:
                st.success("Successfully uploaded images! Refresh to view changes.")
            else:
                st.error(f"The following files failed to upload, please try again: {failed_uploads}")


def display_images_section():
    st.markdown("## Stored Images:")
    order_by_option = st.selectbox("Attribute to order by:", options=["Date Added", "Size", "Filename"])
    

    display_all = st.checkbox("Display all images?")
    if not display_all:
        num_imgs_to_display = st.number_input("Number of images to display:", min_value=0)
    else:
        num_imgs_to_display = None 


    display_original_size = st.checkbox("Display images in original size?")
    if not display_original_size:
        resize_width = st.number_input("Enter desired image width (in pixels):", min_value=100, max_value=500) 
    else:
        resize_width = None

    fn_to_img = storage.get_images(num_imgs_to_display, order_by_option)

    if len(fn_to_img) == 0:
        st.markdown("### -- Nothing to display! --")
    else:
        cols = st.columns(2)
        col_heights = [0, 0]
        for fn, _img in fn_to_img.items():
            curr_col = 0 if col_heights[0] <= col_heights[1] else 1
            img = _img if resize_width == None else resize_img_to_width(_img, resize_width)
            cols[curr_col].image(img, caption=fn)
            col_heights[curr_col] += img.height


def delete_image_section(filename: str):
    if filename:
        if st.button(f"Delete {filename}?"):
            if storage.delete_image(filename):
                st.success(f"Deleted {filename}! Refresh to view changes.")
            else:
                st.error("Could not complete deletion.")


def delete_all_section() -> bool:
    if st.button("Clear Database"):
        confirmation = st.sidebar.text_input("Please type 'Clear Database' to confirm your intent:")
        if confirmation != "Clear Database":
            st.error("Incorrect input! Please try again!")
        else:
            failed_deletions = storage.delete_all_images()
            if not failed_deletions:
                st.success("Cleared all images in database! Please refresh to view changes.")
            else:
                st.error(f"Was able to delete alll images except the following: {failed_deletions}")



