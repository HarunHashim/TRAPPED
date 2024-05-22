FROM python:3.11

WORKDIR /usr/src/app

# Find more efficient way to add files since ./ is not working at the moment.

COPY TRAPPED.py /usr/src/app/

COPY character_malePerson_hit.png /usr/src/app/
COPY character_malePerson_idle.png /usr/src/app/
COPY character_malePerson_run0.png /usr/src/app/
COPY grunt.wav /usr/src/app/
COPY why.png /usr/src/app/
COPY Trapped.mp3 /usr/src/app/

#Attempt to get sound to work but sound gets abit complicated to implement when working with containers

# RUN apt-get update && apt-get install -y alsa-utils

# ENV SDL_AUDIODRIVER=alsa

RUN pip install pygame

RUN apt-get update && apt-get install -y git

CMD ["python", "./TRAPPED.py"]