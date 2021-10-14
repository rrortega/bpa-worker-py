FROM python:3.8-alpine
MAINTAINER Rolando Rodriguez "rolymayo11@gmail.com"

COPY requirements.txt /var/tmp/requirements.txt
RUN pip install --no-cache-dir -r /var/tmp/requirements.txt
WORKDIR "/"
CMD ["python", "main.py"]
