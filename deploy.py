# After making changes to your helm chart or `config.yaml`:
#
# helm repo add jupyterhub https://jupyterhub.github.io/helm-chart
# helm repo update
# (cd ohjh && helm dep up)
# helm upgrade --install --namespace jhub ohjh ohjh --version=v0.1.0 -f secrets.yaml




# helm upgrade ohjhub jupyterhub/jupyterhub --version=v0.6.0-baa1618 -f config.yaml -f secrets.yaml
#
