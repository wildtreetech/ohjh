# OpenHumans Token Refresher

This image contains the OAuth token refresher service.

The image has to be pushed to docker hub in order for JupyterHub to be able to
use it.


# Image contents

The image contains a simpel tornado based web app that users can request their
OpenHumans OAuth tokens from. Internally it talks to JupyterHub to obtain the
tokens. If the tokens are expired it also takes care of renewing them before
passing them to the user. It will also update the auth state of the JupyterHub
with the refreshed tokens.


# Updating the image

Open a terminal in this directory and run:
```
docker build -t betatim/openhumans-refresher:vXXX .
```
Replacing `vXXX` with the next available tag after checking [dockerhub](https://hub.docker.com/r/betatim/openhumans-refresher/)
for tags that are already used.

Now push the image to docker hub: `docker push betatim/openhumans-refresher:vXXX`.

Update the hub image entry in `ohjh/templates/refresher/deployment.yaml`
and run `helm deploy ...`.
