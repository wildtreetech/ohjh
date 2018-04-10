# OpenHumans Singleuser Image

The contents of this image is what is available to people when they start
their notebook.

The image has to be pushed to docker hub in order for JupyterHub to be able to
use it.


# Image contents

The image is based on https://hub.docker.com/r/jupyter/datascience-notebook/.
You can find the source for this image [here](https://github.com/jupyter/docker-stacks/tree/master/datascience-notebook).
At the very least we have to add jupyterhub and the oauth token refresher to
this image or any other image we want to use.

The datascience image has python, R and Julia installed with a reasonable set
of libraries for each.


# Updating the image

Open a terminal in this directory and run:
```
docker build -t betatim/openhumans-singleuser:vXXX .
```
Replacing `vXXX` with the next available tag after checking [dockerhub](https://hub.docker.com/r/betatim/openhumans-singleuser/)
for tags that are already used.

Now push the image to docker hub: `docker push betatim/openhumans-singleuser:vXXX`.

Update the singleuser image entry in `ohjh/values.yaml` and run `helm upgrade ...`.
