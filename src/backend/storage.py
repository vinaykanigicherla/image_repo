import streamlit as st
import json
import boto3 
import numpy as np

from . import image_search

from io import BytesIO
from PIL import Image 
from botocore.errorfactory import ClientError
from typing import Dict, List

s3 = boto3.client('s3',
                region_name = st.secrets["aws_region_name"],
                aws_access_key_id = st.secrets["aws_access_key_id"],
                aws_secret_access_key = st.secrets["aws_secret_access_key"])

model = image_search.load_vectorization_model()


def exists(filename: str) -> bool:
    """Check if object with key filename exists in s3"""
    try:
        response = s3.get_object(Bucket = st.secrets["aws_s3_bucket_name"], Key = filename)
    except ClientError:
        return False 
    
    return True 

def get_all_image_objects():
    """Get all objects of images in s3"""
    objects = s3.list_objects(Bucket = st.secrets["aws_s3_bucket_name"])
    if "Contents" in objects:
        return [obj for obj in objects["Contents"] if obj["Key"].split(".")[1] in {"png", "jpg"}]
    else:
        return [] 
        

def num_images() -> int:
    """Get number of images in s3"""
    return len(get_all_image_objects())


def get_image(filename: str) -> Image.Image:
    """Load in image with filename from s3 bucket"""
    try:
        response = s3.get_object(Bucket = st.secrets["aws_s3_bucket_name"], Key = filename)
        obj = response["Body"].read()
    except ClientError as e:
        return None    
    
    return Image.open(BytesIO(obj))

def get_image_vector(filename: str) -> np.ndarray:
    """Load in image vector corresponding to image with filename"""
    try:
        response = s3.get_object(Bucket = st.secrets["aws_s3_bucket_name"], Key = filename[:-4]+".npy")
        obj = response["Body"].read()
    except ClientError as e:
        return None 

    return np.load(BytesIO(obj))

def get_images(num_imgs: int, order_by: str = "Date Created") -> Dict[str, Image.Image]:
    """Load in first n of all images ordered by some option"""
    _filenames = [f for f in get_all_image_objects()]
    if order_by == "Date Created":
        _filenames.sort(key=lambda x: x["LastModified"], reverse=True)
    if order_by == "Size":
        _filenames.sort(key=lambda x: x["Size"], reverse=True)
    if order_by == "Filename":
        _filenames.sort(key=lambda x: x["Key"], reverse=False)
    
    filenames = [f["Key"] for f in _filenames[:num_imgs]]

    return {fn: get_image(fn) for fn in filenames}


def delete_image(filename: str) -> bool:
    """Delete image with key filename and corresponding vector from s3"""
    try:
        s3.delete_object(Bucket = st.secrets["aws_s3_bucket_name"], Key = filename)
        s3.delete_object(Bucket = st.secrets["aws_s3_bucket_name"], Key = filename[:-4]+".npy")
    except ClientError:
        return False 
    
    return True 

def delete_all_images() -> List[str]:
    """Delete all images and correspinding vectors in s3"""
    filenames = [f["Key"] for f in get_all_image_objects()]
    failed_deletions = []

    for fn in filenames:
        if not delete_image(fn):
            failed_deletions.append(fn)
    
    return failed_deletions

def put_image(img: Image.Image, filename: str) -> bool:
    """Upload img to s3 bucket with key as filename"""   

    in_mem_file = BytesIO()
    img.save(in_mem_file, format = img.format)
    in_mem_file.seek(0)

    in_mem_file_vec = BytesIO()
    np.save(in_mem_file_vec, image_search.vectorize(img, model))
    in_mem_file_vec.seek(0)

    try:
        s3.upload_fileobj(in_mem_file, Bucket = st.secrets["aws_s3_bucket_name"], Key = filename)
        s3.upload_fileobj(in_mem_file_vec, Bucket = st.secrets["aws_s3_bucket_name"], Key = filename[:-4]+".npy")
    except ClientError as e:
        return False 

    return True

def put_images(imgs: List[Image.Image], filenames: List[str]) -> List[str]:
    """Upload all images in imgs to s3"""
    failed_uploads = []
    
    for img, fn in zip(imgs, filenames):
        if not put_image(img, fn):
            failed_uploads.append(fn)

    return failed_uploads

def get_similar_imgs(img: Image.Image, n: int) -> List[Image.Image]:
    """Get n most similar images to img from s3"""
    model = image_search.load_vectorization_model()
    target_vector = image_search.vectorize(img, model)
    
    filenames = [f["Key"] for f in get_all_image_objects()]

    filename_to_vector = {fn: get_image_vector(fn) for fn in filenames}
    filename_to_sim = image_search.find_similarities(filename_to_vector, target_vector)
    filenames.sort(key=lambda fn: filename_to_sim[fn], reverse=True)

    return {fn: get_image(fn) for fn in filenames[:n]}
    





