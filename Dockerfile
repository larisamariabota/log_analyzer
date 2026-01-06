FROM python:3.12-slim

WORKDIR /app

COPY . .

RUN mkdir -p exports

CMD ["python", "main.py"]
