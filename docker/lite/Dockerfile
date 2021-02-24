FROM python:3.7.9-slim

RUN apt-get update && apt-get install -y \
  gcc \
  pv \
  git

RUN pip install jupyter

RUN git clone https://github.com/usc-isi-i2/kgtk/ --branch dev

RUN cd /kgtk && python setup.py install --lite

ARG NB_USER=jovyan
ARG NB_UID=1000
ENV USER ${NB_USER}
ENV NB_UID ${NB_UID}
ENV HOME /home/${NB_USER}

RUN adduser --disabled-password \
    --gecos "Default user" \
    --uid ${NB_UID} \
    ${NB_USER}
    
COPY . ${HOME}
USER root
RUN chown -R ${NB_UID} ${HOME}
RUN chown -R ${NB_UID} kgtk
USER ${NB_USER}
