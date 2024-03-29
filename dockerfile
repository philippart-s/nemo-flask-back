FROM --platform=linux/x86_64 python:3.8

WORKDIR /workspace

RUN pip3 install --upgrade pip

RUN apt-get update 
RUN apt-get install libsndfile-dev -y

ADD . /workspace/

RUN pip3 install -r requirements.txt
RUN chown -R 42420:42420 /workspace

ENV HOME=/workspace

CMD [ "python3" , "/workspace/nemo-back-api.py" ]