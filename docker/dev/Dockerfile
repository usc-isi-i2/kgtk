FROM continuumio/miniconda3

RUN apt-get update && apt-get install -y \
  libxdamage-dev \
  libxcomposite-dev \
  libxcursor1 \
  libxfixes3 \
  libgconf-2-4 \
  libxi6 \
  libxrandr-dev \
  libxinerama-dev \
  pv \
  gcc 

RUN pip install thinc==7.4.0

RUN git clone https://github.com/usc-isi-i2/kgtk/ --branch dev

RUN cd /kgtk && python setup.py install 

RUN conda update -n base -c defaults conda

RUN conda install -c conda-forge graph-tool

RUN conda install -c conda-forge jupyterlab

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
