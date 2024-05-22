FROM python:3.11

ADD TRAPPED.py .

COPY . .

RUN pip install pygame

RUN apt-get update && apt-get install -y git

CMD ["python", "./TRAPPED.py"]