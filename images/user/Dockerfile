FROM jupyter/datascience-notebook:65f1c4bea0b2

# pin jupyterhub to match the Hub version
# set via `docker build --build-arg ...`
ARG JUPYTERHUB_VERSION=0.8.1
RUN pip install --no-cache jupyterhub==$JUPYTERHUB_VERSION

RUN pip install git+https://github.com/OpenHumans/jhoauth-refresh@3ce0b6f7d42f0416cf056dcb887cfefb62b8b513
RUN jupyter serverextension enable --py jhoauthrefresh --sys-prefix

RUN R -e "install.packages(c('stringr', 'tidytext', 'purrr', 'widyr'), repos = 'http://cran.us.r-project.org')"
