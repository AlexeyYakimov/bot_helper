FROM python:3.10-alpine

WORKDIR /db
WORKDIR /app

COPY requirements.txt /app
RUN pip3 install -r requirements.txt

COPY .. /app

CMD ["python3","main.py"]