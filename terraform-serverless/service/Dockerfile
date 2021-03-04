
FROM python:3.8-slim

ENV PORT 8080

COPY . ./

RUN pip install -r requirements.txt

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 app:app
