## KGTK as a Docker image

Docker file for the dev branch of KGTK. The reason for having this Dockerfile is to test new features without having to do a release or build the code locally.

The Docker file builds from the dev branch: `RUN git clone https://github.com/usc-isi-i2/kgtk/ --branch dev` and does a full KGTK installation.



