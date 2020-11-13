FROM python:3.6-alpine

LABEL version="1.0"
LABEL description="Example API REST applications that only has the / endpoint, which responds with a fixed message"

EXPOSE 5000

RUN mkdir /app
WORKDIR /app

COPY code .

RUN pip install -r requirements.txt

ENTRYPOINT ["python","main.py"]
