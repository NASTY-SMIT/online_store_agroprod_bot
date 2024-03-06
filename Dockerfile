FROM python:3.10

WORKDIR /usr/src/app

COPY requirements.txt .
COPY .env .

RUN pip install --no-cache-dir -r requirements.txt

ENV $(cat .env | xargs)

COPY src/ .

RUN python sql.py

EXPOSE 80

ENV NAME World

CMD ["python", "bot.py"]
