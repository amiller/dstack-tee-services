FROM ghcr.io/foundry-rs/foundry:latest

ENV PYTHONUNBUFFERED=1
RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python
RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip setuptools

RUN mkdir /app
WORKDIR /app

ADD requirements.txt /app/
RUN pip install -r requirements.txt

ADD main.py /app/

EXPOSE 5000
ENTRYPOINT []
CMD ["python", "/app/main.py"]
