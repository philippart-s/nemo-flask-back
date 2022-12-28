# nemo-flask-back
Source code in Python using flask for the Nemo's back-end

## Requirements GitPod

    - install libsndfile-dev : `sudo apt-get install libsndfile-dev`
    - install requirements with pip : `pip install -r requirements.txt`

## Requirements MacOs M1

    - installation de libsndfile : `brew install libsndfile`
    - add env variable : `export DYLD_LIBRARY_PATH="/opt/homebrew/lib:$DYLD_LIBRARY_PATH"`
    - installation de tensorflow : `pip install tensorflow-macos`

## Docker

    - build image : `docker build . -t wilda/nemo-back-end:1.1.0` or for Mac M1 `docker buildx build --platform linux/amd64 . -t wilda/nemo-back-end:1.1.0`
    - run image : `docker run -p8080:8080 wilda/nemo-back-end:1.1.0`
    
## OVHcloud :
  - list the container data storage that contain the trained model: 'ovhai data list GRA nemo-data'
  - run: ` ovhai app run --name nemo-back-end --unsecure-http --gpu 1 -p 8080 --volume nemo-data@GRA/:/workspace/data:RW:cache -e DATA_PATH=/workspace/data wilda/nemo-back-end:1.1.0`

## Local

    - create / update the following environment variables:
        - `export DATA_PATH=<path to the data, data for example (default if no car is set)>`
        - `export PATH=$PATH:/Users/stef/Library/Python/3.8/bin`
    - run `python3 nemo-back-api.py`

## End-Points

**⚠️ Always upload a sound before asking a prediction ⚠️**

  - upload a sound
    - resource : _send-sound_
    - _POST_ request
    - payload : image in binary format

  - do a prediction
    - resource : _get-animal-name_
    - _GET_ request
