FROM python:3.6-alpine
MAINTAINER Ondrej Sika <ondrej@ondrejsika.com>
WORKDIR /app
COPY index.py /app/index.py
CMD ["python", "index.py"]

