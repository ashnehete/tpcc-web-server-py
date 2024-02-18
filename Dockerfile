FROM python:3.11-slim-bookworm

WORKDIR /app
COPY ./requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY src/ .

CMD ["gunicorn", "app:app"]