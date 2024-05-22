FROM python:3.11

ADD TRAPPED.py .

RUN pip install pygame

RUN apt-get update && apt-get install -y git

CMD ["python", "./TRAPPED.py"]