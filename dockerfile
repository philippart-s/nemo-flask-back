FROM python:3.8

WORKDIR /workspace
ADD requirements.txt /workspace/requirements.txt

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

ADD nemo-back-api.py saved_model csv_files /workspace/

RUN apt-get update 
RUN apt-get install libsndfile-dev -y

RUN chown -R 42420:42420 /workspace
ENV HOME=/workspace
CMD [ "python3" , "/workspace/nemo-back-api.py" ]