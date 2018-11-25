FROM python:3.6-alpine
ADD . /code
WORKDIR /code
VOLUME /code
EXPOSE 5000
RUN pip install -r requirements.txt
CMD ["python", "mquery.py"]
