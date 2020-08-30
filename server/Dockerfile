FROM python:3.6-slim-stretch

RUN apt-get update -y
RUN apt-get install -y python3 python-pip-whl python3-pip
RUN apt-get install -y libusb-1.0-0-dev libudev-dev

WORKDIR /app

COPY requirements.txt /app/
RUN pip3 install -r requirements.txt

COPY . /app

RUN chmod +x /app/app.py

ENTRYPOINT [ "python3" ]
CMD [ "app.py" ]
