FROM python:3.11.8-slim-bullseye

ENV PYTHONBUFFERED 1
ENV PORT 8001

WORKDIR /django_server/app

COPY requirements.txt /django_server/app/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY ./django_server /django_server/app
EXPOSE ${PORT}

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
