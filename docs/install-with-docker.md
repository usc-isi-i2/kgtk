## Installing and Using KGTK with Docker

### Installing Docker

If you do not have Docker installed, follow the directions at:

```bash
https://docs.docker.com/get-docker/
```

### Installing KGTK from the Docker Hub

Pull the latest KGTK image with this command:

```bash
docker pull uscisii2/kgtk:latest
```

### Run KGTK on a Docker Command Line

To run KGTK in the command line type (note that if you built the image
yourself, you should replace `uscisii2/kgtk:latest` by `kgtk-local` in this
and the following commands):

```bash
docker run -it --rm  --user root -e NB_GID=100 -e GEN_CERT=yes -e GRANT_SUDO=yes uscisii2/kgtk:latest /bin/bash
```

### Accessing Local Data with the Docker Command Line

If you want to load data from your local machine, you will need to [mount a volume](https://docs.docker.com/storage/volumes/).
For example, to mount the current directory (`$PWD`) and launch KGTK in command line mode:

```bash
docker run -it --rm -v $PWD:/out --user root -e NB_GID=100 -e GEN_CERT=yes -e GRANT_SUDO=yes uscisii2/kgtk:latest /bin/bash
```

### Runnning KGTK in a Jupyter Notebook using Docker

If you want to run KGTK in a **Jupyter notebook**, mounting the current directory (`$PWD`) as a folder called `/out` then you will have to type:

```bash
docker run -it -v $PWD:/out -p 8888:8888 uscisii2/kgtk:latest /bin/bash -c "jupyter notebook --ip='*' --port=8888 --no-browser"
```

You will see a message similar to:

```bash
[C 22:36:40.418 NotebookApp]

    To access the notebook, open this file in a browser:
        file:///root/.local/share/jupyter/runtime/nbserver-1-open.html
    Or copy and paste one of these URLs:
        http://092260f3740e:8888/?token=83945df95e9b1f5f7594597d3925960fc89dbefaed4ada7d
     or http://127.0.0.1:8888/?token=83945df95e9b1f5f7594597d3925960fc89dbefaed4ada7d
```

Copy the localhost URL (in the case above `http://127.0.0.1:8888/?token=83945df95e9b1f5f7594597d3925960fc89dbefaed4ada7d`, this is random every time) and paste it in your browser. In order to run KGTK commands in a notebook, remember to add `%%bash` in the line before your command, as shown below:

```bash
%%bash
kgtk --help
```

As a result, now you should be able to see a help message similar to the one depicted below:

![Diagram](images/nb.png)

!!! note
    if you want to load data from your local machine or save the results obtained with KGTK, you will need to [mount a volume](https://docs.docker.com/storage/volumes/) as described above. **Notebooks stored inside the container will be erased after the container finishes its execution**.

!!! note
    Older versions of KGTK (0.3.2 and 0.2.1) require `--allow-root` as part of the jupyter notebook command `jupyter notebook --ip='*' --port=8888 --allow-root --no-browser`

### Additional Docker Images

More information about all available versions and tags is available here:
[https://hub.docker.com/repository/docker/uscisii2/kgtk](https://hub.docker.com/repository/docker/uscisii2/kgtk). For
example, the `dev` branch is available at `uscisii2/kgtk:latest-dev`.

## Building a Docker Image

You can build a local Docker image after installing KGTK from GitHub.
Use the following commands starting from your KGTK installation
folder:

```
cd docker/
docker build -t kgtk-local .
```

## Updating your KGTK installation

To update your version of KGTK, then just pull the most recent image:

`docker pull <image_name>`]

where `<image_name>` is the tag of the image of interest (e.g. uscisii2/kgtk:latest)
