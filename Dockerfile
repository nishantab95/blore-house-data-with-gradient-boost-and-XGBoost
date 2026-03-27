FROM python:3.10

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONUNBUFFERED=1

CMD exec gunicorn --workers 4 --bind :${PORT:-8080} app.app:app