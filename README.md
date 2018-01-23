# The OpenHumans JupyterHub deployment

This repo will describe how to deploy JupyterHub for openhumans.org.


## Structure

Most of the configuration happens in `config.yaml`.

To create a new cluster from scratch read [create.md](create.md).

To tear everything down again: [destroy.md](destroy.md).

If you make changes and want to deploy them checkout `deploy.py`.


## Secrets

You will need `secrets.yaml` to make the configuration complete. For the moment
this file is not part of the git repository. Contact Tim if you need a copy.
