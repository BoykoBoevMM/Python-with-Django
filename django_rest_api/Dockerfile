FROM python:3.11.8-slim-bullseye

ENV PYTHONBUFFERED 1

ENV PORT 8000

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /app/
EXPOSE ${PORT}

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

