FROM jupyter/datascience-notebook:65f1c4bea0b2

# pin jupyterhub to match the Hub version
# set via `docker build --build-arg ...`
ARG JUPYTERHUB_VERSION=0.8.1
RUN pip install --no-cache jupyterhub==$JUPYTERHUB_VERSION

RUN pip install git+https://github.com/OpenHumans/jhoauth-refresh@ba3bd3782a31612abeca8eb13a41b56ec68947df
RUN jupyter serverextension enable --py jhoauthrefresh --sys-prefix
