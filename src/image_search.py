import streamlit as st 
import numpy as np

from tensorflow.keras.applications.resnet50 import ResNet50
from PIL import Image 
from typing import Dict

def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """Compute similarity between vector a and b"""
    return float(np.dot(a, b.T)/(np.linalg.norm(a)*np.linalg.norm(b)))

def load_vectorization_model():
    """Load ResNet50 model with Imagenet weights for vectorizing images"""
    return ResNet50(include_top=False, weights="src/res/resnet50_weights_tf_dim_ordering_tf_kernels_notop.h5", pooling="avg")

def vectorize(img: Image.Image, model) -> np.ndarray:
    """Vectorize img using ResNet50 model"""
    img = img.resize((224,224))
    np_arr = np.array(img).reshape(1, 224, 224, 3)
    return model.predict(np_arr)

def find_similarities(filename_to_vector: Dict[str, np.ndarray], target: np.ndarray) -> Dict[str, float]:
    """Find similarity between target vector and image vector associated with each filename"""
    filename_to_sim = dict()
    for fn in filename_to_vector:
        filename_to_sim[fn] = cosine_similarity(filename_to_vector[fn], target)

    return filename_to_sim
