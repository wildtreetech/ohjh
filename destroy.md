# How to stop everything and delete all traces

These instructions are probably irrelevant for the production cluster as they
will remove everything, including user's home directories. The instructions
are useful for peple experimenting with new setups who want to remove their
test cluster (so that they don't keep costing money).

```
$ kubectl delete ns <your-namespace>
```

If you followed this guide your namespace is probably called `jhub`. You can
find out by runnign `kubectl get pods --all-namespaces`. Your namespace is the
one containing a pod called `hub-78c4f848d7-j2xtt` or similar.

Next delete your kubernetes cluster. Adjust the following command by replacing
`jhub` with the name of your cluster.
You also need to set the zone in which the cluster is.
```
$ gcloud container clusters delete jhub --zone=us-central1-b
```

Now delete your project on Google cloud.
