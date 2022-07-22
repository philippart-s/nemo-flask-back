# nemo-flask-back
Source code in Python using flask for the Nemo's back-end

## Docker

    - build image : `docker build . -t wilda/nemo-back-end:1.0.0`
    - run de l'image : `docker run -p8080:8080 wilda/nemo-back-end:1.0.0`
## OVHcloud :

  - lancement : `ovhai app run --unsecure-http --gpu 1 -p 8080 wilda/nemo-back-end:1.0.0`

## End-Points

**⚠️ Always upload a sound before asking a prediction ⚠️**

  - upload a sound
    - resource : _send-sound_
    - _POST_ request
    - payload : image in binary format

  - do a prediction
    - resource : _get-animal-name_
    - _GET_ request
