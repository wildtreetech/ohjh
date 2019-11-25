# The *I have no idea what I'm doing guide to pushing changes*

![](http://img.memecdn.com/i-have-no-idea-what-im-doing_o_865021.gif)

Luckily there's a lot of documentation on [how to setup a JupyterHub](https://zero-to-jupyterhub.readthedocs.io/). But none of these are really targeted at users who might want to just administer an existing setup. Which makes it hard to find out where to dive in.

Here's a quick guide for what to do if you have done all the changes to this repo that you want to do but haven't set up your connection to Google Cloud, Kubernetes etc.

## Install the CLI for Google Cloud

The best way to interact with the JupyterHub setup and your local changes is through the Google Cloud CLI which you can [install through the `Google Cloud SDK`](https://cloud.google.com/sdk/).

After downloading and unzipping do

```
cd google-cloud-sdk
./install.sh
```

to install the CLI tool. Once that's done you can log in into your Google account by running

```
gcloud init
```

which will take you to the Google website to login and authenticate your CLI. Now you should also install the Kubernetes tools and setup your cluster credentials:

```
gcloud components install kubectl
gcloud container clusters get-credentials jhub --zone us-central1-b --project open-humans-jupyterhub
```

## Setup your Helm installation

`helm` is the tool used for interfacing with the Kubernetes installation on Google Cloud.

To install it run

```
curl https://raw.githubusercontent.com/kubernetes/helm/master/scripts/get | bash
```

Once that's done you can run the following to setup your `helm` installation:

```
helm init --client-only --service-account tiller
helm version
```

You should see the versions of helm that you run locally on your computer and the one that's setup on your cluster printed to your shell now. If you find that your server's version is older than your local one you can (and need to!) update the remote version using the following command:

```
helm init --upgrade
```

## Actually pushing your changes
With all that out of the way you can now push your changes! 🎉

Setup the helm deps from the root of this repository:

```
helm repo add jupyterhub https://jupyterhub.github.io/helm-chart
helm repo update
```

Then move into the `ohjh` subfolder, run `dep up` and move back to the root:

```
cd ohjh
helm dep up
cd ..
```

Now you can actually upgrade the helm:

```
helm upgrade --install --namespace jhub ohjh ohjh --version=v0.1.0 -f secrets.yaml
```

Notice that you need to specify the `secrets.yaml` that needs to be present in the root-directory of this repository! Also the version should match the one in `ohjh/Chart.yaml`.

And that's it. It should deploy the changes and the next time you start a notebook server the changes will be applied!

## Restarting stuff
It can happen ( at least it happened to [@gedankenstuecke](https://www.github.com/gedankenstuecke)) that the whole JupyterHub becomes stuck - either due to an update or just because. To fix this you can use the `kubectl` command on your local machine. You can `delete` pods, they will be restarted by kubernetes.

To see all the pods currently running:

```
kubectl --namespace=jhub get pod
```

To get details for a single pod you can use `describe`:

```
kubectl --namespace=jhub describe pod jupyter-emeadows317
```

To delete things you can use `delete` along with a `label` that you can see in the output of `describe` (e.g. `app` or `component` etc.)

### Examples
To delete all `singleuser-server`:

```
kubectl --namespace=jhub delete pods -l component=singleuser-server
```

To delete all pods associated with JupyterHub:

```
kubectl --namespace=jhub delete pods -l app=jupyterhub
```


## Identifying & killing pods used for mining

Once Google Cloud sends an email about a potential abuse of the Hub for mining, you
might want to find which user is responsible for this. In a first step we need to find
out the pod-name of our hub itself. This can be done by running:

`kubectl get pods`

In return you will get all pods currently running, including the hub.
The name of the pod is made up at random, but looks something like

`hub-5f465d499f-2d8pm`

Use this name to grep in the log files to find which users have logged in/started their pods
at the time the abuse was found:

`kubectl logs hub-5f465d499f-2d8pm | grep " Adding user"`

E.g. you will get a return of the form

```
[I 2019-11-25 08:17:31.105 JupyterHub proxy:242] Adding user gedankenstuecke to proxy /user/gedankenstuecke/ => http://hub-5f465d499f-2d8pm:56425
```

Now that you have a list of the usernames you can delete individual user pods like shown above:

```
kubectl delete pod jupyter-gedankenstuecke
```

This immediately stops the pod of the user. Ideally you have deactivated that user's Open Humans account prior to this, so that they can't spawn a new one. 
