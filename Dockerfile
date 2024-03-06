FROM python:3-slim-buster

WORKDIR /bot
COPY . /bot/
RUN apt update && apt install ffmpeg -y && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
RUN mv .env.example .env
RUN pip install --upgrade pip && pip install -r requirements.txt

CMD [ "python", "./bot.py" ]
