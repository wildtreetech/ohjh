FROM python:3.6-alpine3.6

RUN pip3 install --no-cache-dir \
        tornado \
        requests \
        https://github.com/jupyterhub/jupyterhub/archive/b26b1bc038029fe6ff790b195591ca48250fdd15.zip#egg=jupyterhub

ADD whoami.py /srv/whoami.py

CMD python3 /srv/whoami.py
