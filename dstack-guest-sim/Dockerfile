FROM python:3.7

RUN mkdir /app
WORKDIR /app

COPY requirements.txt /app/
RUN pip install -r requirements.txt

ADD main.py /app/

EXPOSE 5001
CMD ["python", "/app/main.py"]
