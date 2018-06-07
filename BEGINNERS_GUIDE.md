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
