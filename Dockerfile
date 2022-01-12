FROM python:3.9
RUN mkdir filter
WORKDIR filter
COPY ./requirements.txt /filter
COPY . /filter
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y
RUN pip3 install --upgrade pip -r requirements.txt
EXPOSE 5000