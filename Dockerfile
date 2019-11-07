FROM python:3.7.5-slim-buster
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD python ./tests/test_ebook.py 
