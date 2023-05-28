FROM --platform=$BUILDPLATFORM python:3.10-alpine

WORKDIR /db
WORKDIR /app

COPY requirements.txt /app
RUN --mount=type=cache,target=/root/.cache/pip \
    pip3 install -r requirements.txt

COPY .. /app

CMD ["python3","main.py"]