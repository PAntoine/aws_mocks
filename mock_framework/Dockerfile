FROM alpine:3.12

RUN apk add --no-cache openssh python3 py3-pip

COPY . /app
WORKDIR /app
RUN python3 setup.py install

EXPOSE 5000

CMD ["python3","app.py"]
