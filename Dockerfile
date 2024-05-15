FROM python:3.11-slim-bookworm

WORKDIR /app
COPY ./requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY src/ .
RUN mkdir -p data

CMD ["gunicorn", "--bind=0.0.0.0:8000", "app:app"]