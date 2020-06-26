FROM python:3.6.10-slim

RUN apt-get update && apt-get install -y \
  gcc \
  git

RUN pip install jupyter

RUN git clone https://github.com/usc-isi-i2/kgtk/ --branch feature/lite

RUN cd /kgtk && python setup.py install --lite