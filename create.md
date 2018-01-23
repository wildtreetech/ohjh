# Creating a JupyterHub deployment

These are steps you need to perform to setup a new cluster from scratch. This
is probably not needed very often for the production system. It exists primarily
as a record of how it was done and for use with test deployments.

A good guide, maintained by the JupyterHub team on how to setup JupyterHub from
zero is: https://zero-to-jupyterhub.readthedocs.io/en/v0.5-doc/ This document
is a condensed version of that guide.


## Create a project on Google cloud

XXX


## Configure your gcloud and kubectl tools

Make sure that you are talking to your newly created project. To list your
projects `gcloud projects list`. Use the name from the PROJECT_ID column.
If your project is called `open-humans-jupyterhub` run:

```
gcloud config set project open-humans-jupyterhub
```

Setup for using the jhub cluster in the open-humans-jupyterhub project:
```
gcloud container clusters get-credentials jhub --zone us-central1-b --project open-humans-jupyterhub
```


## create cluster on gcloud

```
gcloud container clusters create jhub \
    --num-nodes=3 --machine-type=n1-standard-2 \
    --zone=us-central1-b --cluster-version=1.8.6-gke.0
```


## Install helm

[Full details](https://zero-to-jupyterhub.readthedocs.io/en/v0.5-doc/setup-helm.html#setup-helm)
on setting up helm both locally and on your cluster.
```
# create tiller accounts
kubectl --namespace kube-system create sa tiller
kubectl create clusterrolebinding tiller --clusterrole cluster-admin \
    --serviceaccount=kube-system:tiller
helm init --service-account tiller
```

Verify this worked with `helm verify`. You might have to wait a minute or two
for this command to succeed.

Secure tiller:
```
kubectl --namespace=kube-system patch deployment tiller-deploy --type=json --patch='[{"op": "add", "path": "/spec/template/spec/containers/0/command", "value": ["/tiller", "--listen=localhost:44134"]}]'
```


## Install JupyterHub

[Full guide](https://zero-to-jupyterhub.readthedocs.io/en/v0.5-doc/setup-jupyterhub.html#setup-jupyterhub)

Use the `config.yaml` in this repository. You will need to update it to insert
the secret token for the proxy. You should also change the hostname and contact
details for HTTPS or remove that section for a test deployment. Read the
[HTTPS setup details](https://zero-to-jupyterhub.readthedocs.io/en/v0.5-doc/security.html#https)
for automatic HTTPS (letsencrypt). Furthermore you can't find out the external
IP of your JupyterHub cluster until after you start it. This means you can not
setup your domain to point to the cluster. This means put adding HTTPS on the
list of things to do after creating your cluster.

Add the JupyterHub helm chart:
```
helm repo add jupyterhub https://jupyterhub.github.io/helm-chart/
helm repo update
```

Now you are ready to instal JupyterHub
```
helm install jupyterhub/jupyterhub --version=v0.6.0-baa1618 \
    --name=ohjhub --namespace=jhub -f config.yaml
```

To find the external IP of your cluster to setup your domain name and HTTPS:
```
kubectl --namespace=jhub get svc
```
Look at the EXTERNAL_IP column.
