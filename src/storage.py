import streamlit as st
import json
import boto3 

from io import BytesIO
from PIL import Image 
from botocore.errorfactory import ClientError

from typing import Dict, List

from utils import is_image_file


s3 = boto3.client('s3',
                region_name = st.secrets["aws_region_name"],
                aws_access_key_id = st.secrets["aws_access_key_id"],
                aws_secret_access_key = st.secrets["aws_secret_access_key"])


def get_image(filename: str) -> Image.Image:
    """Load in image with filename from s3 bucket"""
    try:
        response = s3.get_object(Bucket = st.secrets["aws_s3_bucket_name"], Key = filename)
        obj = response["Body"].read()
    except ClientError as e:
        obj = []    
    
    return Image.open(BytesIO(obj))

def get_images(num_imgs: int, order_by: str = "Date Created") -> Dict[str, Image.Image]:
    _filenames = [f for f in s3.list_objects(Bucket = st.secrets["aws_s3_bucket_name"])["Contents"]]
    if order_by == "Date Created":
        _filenames.sort(key=lambda x: x["LastModified"], reverse=True)
    if order_by == "Size":
        _filenames.sort(key=lambda x: x["Size"], reverse=True)
    if order_by == "Filename":
        _filenames.sort(key=lambda x: x["Key"], reverse=False)
    
    filenames = [f["Key"] for f in _filenames[:num_imgs]]

    return {fn: get_image(fn) for fn in filenames}


def delete_image(filename: str) -> bool:
    try:
        response = s3.delete_object(Bucket = st.secrets["aws_s3_bucket_name"], Key = filename)
    except ClientError:
        return False 
    
    return True 

def delete_all_images() -> List[str]:
    filenames = [f["Key"] for f in s3.list_objects(Bucket = st.secrets["aws_s3_bucket_name"])["Contents"]]
    failed_deletions = []

    for fn in filenames:
        if not delete_image(fn):
            failed_deletions.append(fn)
    
    return failed_deletions



def image_exists(filename: str) -> bool:
    try:
        response = s3.get_object(Bucket = st.secrets["aws_s3_bucket_name"], Key = filename)
    except ClientError:
        return False 
    
    return True 


def put_image(img: Image.Image, filename: str) -> bool:
    """Upload img to s3 bucket with key as filename"""   

    in_mem_file = BytesIO()
    img.save(in_mem_file, format = img.format)
    in_mem_file.seek(0)

    try:
        s3.upload_fileobj(in_mem_file, Bucket = st.secrets["aws_s3_bucket_name"], Key = filename)
    except ClientError as e:
        return False 
    
    return True

def put_images(imgs: List[Image.Image], filenames: List[str]) -> List[str]:
    failed_uploads = []
    
    for img, fn in zip(imgs, filenames):
        if not put_image(img, fn):
            failed_uploads.append(fn)

    return failed_uploads








