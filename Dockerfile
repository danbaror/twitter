FROM python:3.6-alpine
ADD . /code
WORKDIR /code
VOLUME /code
RUN pip install -r requirements.txt
CMD ["python", "app.py"]
