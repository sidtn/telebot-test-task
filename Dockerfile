FROM python:3.10

RUN mkdir /app
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN python3 -m pip install --upgrade pip
COPY . /app
RUN pip install -r requirements.txt

