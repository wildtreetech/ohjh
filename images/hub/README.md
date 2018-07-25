# OpenHumans Hub Image

This image contains the hub, or JupyterHub itself.

The image has to be pushed to docker hub in order for JupyterHub to be able to
use it.


# Image contents

The image is based on https://github.com/jupyterhub/zero-to-jupyterhub-k8s/tree/master/images/hub.
That image is the official image used in the Zero2JupyterHub guide. We make
our own because we want to use a modified version of oauthenticator which has
not yet been released.

Once there is a release we should switch to the standard
image, or inherit from it.


# Updating the image

Open a terminal in this directory and run:
```
docker build -t betatim/openhumans-hub:vXXX .
```
Replacing `vXXX` with the next available tag after checking [dockerhub](https://hub.docker.com/r/betatim/openhumans-hub/)
for tags that are already used.

Now push the image to docker hub: `docker push betatim/openhumans-hub:vXXX`.

Update the hub image entry in `ohjh/values.yaml` and run `helm deploy ...`.
