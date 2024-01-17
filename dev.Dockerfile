FROM python:3.10.12

WORKDIR /app

# Should be improved in the future
COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
