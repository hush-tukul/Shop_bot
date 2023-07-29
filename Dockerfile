FROM python:3.11
ENV BOT_NAME=$BOT_NAME

WORKDIR /usr/src/app/"${BOT_NAME:-tg_bot}"

COPY requirements.txt /usr/src/app/"${BOT_NAME:-tg_bot}"
RUN pip install -r /usr/src/app/"${BOT_NAME:-tg_bot}"/requirements.txt
COPY . /usr/src/app/"${BOT_NAME:-tg_bot}"

ENV QUART_APP=app.py:app




#FROM python:3.11
#ENV BOT_NAME=$BOT_NAME
#
#WORKDIR /home/payment_bot
#
#COPY requirements.txt .
#RUN pip install -r requirements.txt
#COPY . .
#ENTRYPOINT  ["hypercorn", "--bind", "0.0.0.0:5000",  "app.py:app"]



#ENV QUART_APP=app.py:app


#/usr/src/app/"${BOT_NAME:-tg_bot}"