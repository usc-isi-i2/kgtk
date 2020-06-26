## KGTK-lite as a Docker image

This version of KGTK does not incorporate graph-tool and embeddings to be lighter.

To use this Dockerfile, you can build it yourself: 

```
docker build -t user/myImage .
```

Where `user` corresponds to your DockerHub user and `myImage` to the name you may want to give it.

Alternatively, you can pull the latest image we already built in Dockerhub:

```
docker pull uscisii2/kgtk-lite:0.2.0
```

To run KGTK in the command line just type:

```
docker run -it uscisii2/kgtk /bin/bash
```

If you want to run KGTK in a Jupyter notebook, then you will have to type:
```
docker run -it -p 8888:8888 uscisii2/kgtk /bin/bash -c "jupyter notebook --ip='*' --port=8888 --allow-root --no-browser"
```

Note: if you want to load data from your local machine, you will need to [mount a volume](https://docs.docker.com/storage/volumes/).

More information about versions and tags is available here: https://hub.docker.com/repository/docker/uscisii2/kgtk

See additional examples in [the documentation](https://kgtk.readthedocs.io/en/latest/install/).

