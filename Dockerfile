# Dockerfile content
FROM python:3.10

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

CMD ["python", "manage.py", "migrate","python", "manage.py", "runserver", "0.0.0.0:8000"]
