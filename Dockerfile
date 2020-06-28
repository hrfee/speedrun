FROM python:3.8.2-buster

RUN wget https://github.com/hrfee/speedrun/releases/download/v0.1.0/speedrun-0.1.0-py3-none-any.whl

RUN pip install speedrun-0.1.0-py3-none-any.whl

CMD [ "speedrun-serve" ]
