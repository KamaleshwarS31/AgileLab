FROM python:3.9

WORKDIR /student-app

COPY . .

CMD ["python", "app.py"]
