# nemo-flask-back
Source code in Python using flask for the Nemo's back-end

## Docker

    - build image : `docker build . -t wilda/nemo-back-end:1.0.0` or for Mac M1 `docker buildx build --platform linux/amd64 . -t wilda/nemo-back-end:1.1.0`
    - run de l'image : `docker run -p8080:8080 wilda/nemo-back-end:1.0.0`
    
## OVHcloud :

  - lancement : ` ovhai app run --name nemo-back-end --unsecure-http --gpu 1 -p 8080 --volume nemo-data@GRA/:/workspace/data:RW:cache -e DATA_PATH=/workspace/data wilda/nemo-back-end:1.1.0`

## End-Points

**⚠️ Always upload a sound before asking a prediction ⚠️**

  - upload a sound
    - resource : _send-sound_
    - _POST_ request
    - payload : image in binary format

  - do a prediction
    - resource : _get-animal-name_
    - _GET_ request
