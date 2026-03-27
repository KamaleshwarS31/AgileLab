FROM python:3.10

WORKDIR /student-app

COPY . .

CMD ["python", "app.py"]