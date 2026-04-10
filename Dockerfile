FROM python:3.10-slim

WORKDIR /student-app

COPY . .

CMD ["python", "app.py"]
