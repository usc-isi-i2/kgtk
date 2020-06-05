## KGTK as a Docker image

How to build this docker image:

```
docker build -t uscisii2/kgtk:0.2.0 .
```

How to run this docker image (from DockerHub):

```
docker run -it uscisii2/kgtk:0.2.0 /bin/bash
```

This will log you into the image and let you operate with KGTK. Once you executed the step above, just type:

```
kgtk -h
```

to see the KGTK help command.

## Next features:
We will include the following features in the next releases of KGTK:

- Examples on how to load volumes with your data.

- How to launch a Jupyter notebook to operate with KGTK in your browser.

