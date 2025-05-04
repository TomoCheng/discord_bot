FROM python:3.13-slim

WORKDIR /app

RUN apt-get update

COPY . .

RUN pip install -r requirements.txt

CMD ["python3", "bot.py"]
