# Image Repository!
### Description
A simple image repository capabale of storing and searching over images. The app is [deployed](https://share.streamlit.io/vinaykanigicherla/image_repo/src/app.py) using Streamlit Share. The primary features are:

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

### Running Locally
To run the app using Docker, do:
``` 
$ docker build -t your_docker_image_name:latest .
$ docker run -p 8501:8501 your_docker_image_name:latest
```

To run tests with PyTest simply use the following command:
```
$ pytest
```

### TODO
- The application currently only works for a single user. Add a user login system so each user has control over only their uploaded images.  
