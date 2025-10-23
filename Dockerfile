FROM python:latest
LABEL authors="wjatscheslawschwab"
WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
#CMD ["python", "manage.py", "makemigrations"]
#CMD ["python", "manage.py", "migrate"]
#CMD ["python", "manage.py", "runserver"]
CMD ["gunicorn", "rental_project.wsgi:application", "--bind", "0.0.0.0:8000"]
