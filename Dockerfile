FROM python:3.12-slim

WORKDIR /app

COPY . .



# CMD portabil: rulează main.py, dar permite clientului să dea argumente
ENTRYPOINT ["python", "main.py"]

