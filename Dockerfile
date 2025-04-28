FROM python:3.12-slim

WORKDIR /app

RUN apt-get update

COPY . .

RUN pip install -r requirements.txt

CMD ["python3", "bot.py"]
