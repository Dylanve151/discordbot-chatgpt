FROM python:3-slim-buster

WORKDIR /bot
COPY . /bot/
RUN mv .env.example .env
RUN pip install --upgrade pip && pip install -r requirements.txt

CMD [ "python", "./bot.py" ]
