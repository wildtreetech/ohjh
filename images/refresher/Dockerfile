FROM python:3.7-slim

RUN pip3 install --no-cache-dir \
        requests \
        pyyaml \
        jupyterhub==1.1

ADD whoami.py /srv/whoami.py

CMD python3 /srv/whoami.py
