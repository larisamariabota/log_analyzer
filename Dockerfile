FROM python:3.12-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

# CMD portabil: rulează main.py, dar permite clientului să dea argumente
ENTRYPOINT ["python", "main.py"]

