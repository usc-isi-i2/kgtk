FROM continuumio/miniconda3

RUN apt-get update && apt-get install -y \
  libxdamage-dev \
  libxcomposite-dev \
  libxcursor1 \
  libxfixes3 \
  libgconf-2-4 \
  libxi6 \
  libxrandr-dev \
  libxinerama-dev\
  gcc 

RUN pip install thinc==7.4.0

RUN git clone https://github.com/usc-isi-i2/kgtk/ --branch dev

RUN cd /kgtk && python setup.py install 

RUN conda update -n base -c defaults conda

RUN conda install -c conda-forge graph-tool

RUN conda install -c conda-forge jupyterlab