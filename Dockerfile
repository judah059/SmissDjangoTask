FROM python:3-alpine
ENV PYTHONUNBUFFERED 1
WORKDIR /app
ADD . ./app
RUN pip freeze > requirements.txt