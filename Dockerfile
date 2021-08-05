FROM debian:buster

RUN apt update && \
apt-get install curl gnupg ca-certificates zlib1g-dev libjpeg-dev git python3 python3-pip -y

RUN echo "deb https://packages.cloud.google.com/apt coral-edgetpu-stable main" | tee /etc/apt/sources.list.d/coral-edgetpu.list
RUN curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -

RUN apt-get update && \
apt-get install libedgetpu1-std python3-pycoral -y

RUN apt-get update
RUN groupadd -g 1000 someUser && useradd -u 1000 -g someUser -d /app -m someUser

WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN chown -R someUser:someUser /app

# USER someUser
RUN pip3 install --user -r requirements.txt

USER root
COPY . /app
RUN chown -R someUser:someUser /app

# USER someUser
CMD ["python3", "main.py"]