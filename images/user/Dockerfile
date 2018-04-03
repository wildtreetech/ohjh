FROM jupyter/datascience-notebook:65f1c4bea0b2

# pin jupyterhub to match the Hub version
# set via `docker build --build-arg ...`
ARG JUPYTERHUB_VERSION=0.8.1
RUN pip install --no-cache jupyterhub==$JUPYTERHUB_VERSION

RUN pip install git+https://github.com/betatim/jhoauth-refresh@752037ac222154041ad854229f3caf7d7c327452
RUN jupyter serverextension enable --py jhoauthrefresh --sys-prefix
