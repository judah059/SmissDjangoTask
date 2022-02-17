FROM python:3-alpine
ENV PYTHONUNBUFFERED 1
WORKDIR /forDjango/task_project
ADD . ./forDjango/task_project
RUN pip freeze > requirements.txt