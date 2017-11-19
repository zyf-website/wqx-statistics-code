FROM python:3.6

RUN mkdir /usr/app
WORKDIR /usr/app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.douban.com/simple
