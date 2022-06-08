import streamlit as st 
import numpy as np

from transformers import CLIPProcessor, CLIPModel
from PIL import Image 
from typing import Dict


model = CLIPModel.from_pretrained("src/res/clip-vit-base-patch32").to("cpu")
processor = CLIPProcessor.from_pretrained("src/res/clip-vit-base-patch32")


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """Compute similarity between vector a and b"""
    return float(np.dot(a, b.T)/(np.linalg.norm(a)*np.linalg.norm(b)))

def vectorize_img(img: Image.Image) -> np.ndarray:
    """Vectorize img using CLIP model"""
    inputs = processor(text=None, images=img, return_tensors="pt", padding=True)
    return model.get_image_features(**inputs).detach().numpy()

def vectorize_text(text: str) -> np.ndarray:
    """Vectorize img using CLIP model"""
    inputs = processor(text=[text], images=None, return_tensors="pt", padding=True)
    return model.get_text_features(**inputs).detach().numpy()

def find_similarities(filename_to_vector: Dict[str, np.ndarray], target: np.ndarray) -> Dict[str, float]:
    """Find similarity between target vector and image vector associated with each filename"""
    filename_to_sim = dict()
    for fn in filename_to_vector:
        filename_to_sim[fn] = cosine_similarity(filename_to_vector[fn], target)

    return filename_to_sim
