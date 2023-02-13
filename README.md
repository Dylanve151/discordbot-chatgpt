# discordbot-chatgpt
gives a error somethimes

## Running locally

```bash
pip install discord openai
```

Copy `.env.example` to `.env` and replace variables in the file
* BOT_TOKEN=
* OPENAI_TOKEN=

```bash
python ./bot.py
```

## Running in Docker

Copy `.env.example` to `.env` and replace variables in the file
* BOT_TOKEN=
* OPENAI_TOKEN=

```bash
docker build --tag dylanve151/discordbot-chatgpt .
docker run -d dylanve151/discordbot-chatgpt
```