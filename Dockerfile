FROM python:3.9

COPY . /app

WORKDIR /app

#Install packages from requirements.txt 
RUN pip install --upgrade pip
RUN pip --no-cache-dir install -r requirements.txt

#Expose Streamlit port
EXPOSE 8501

#Run 
ENTRYPOINT ["streamlit", "run"]
CMD ["src/app.py"]