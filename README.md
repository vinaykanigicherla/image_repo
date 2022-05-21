# Image Repository!
A simple image repository capabale of storing and searching over images. The primary features are:

- Addition
  - Single image upload
  - Multiple images upload at once
- Deletion
  - Single image delete
  - Delete all images stored
- Search
  - Text Search: Find an image in the repository with a given filename
  - Reverse Image Search: Find the top N images in the repository that are the most similar to an uploaded query image

All files are stored using AWS S3 and interface is built using Streamlit. 


**TODO:**
- The application currently only works for a single user. Add a user login system so each user has control over only their uploaded images.  
