FROM python:3.10.12

WORKDIR /app

COPY requirements.txt .

RUN pip3 install --no-chache-dir -r requirements.txt

# To-do: Manage to run 'mydb.py' to create the database

# Should be improved in the future
COPY . .

EXPOSE 8000

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
