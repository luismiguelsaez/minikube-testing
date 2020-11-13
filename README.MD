
## Initial setup

### Install minikube

```
$ curl -sL https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64 -o ~/.local/bin/minikube \
  && chmod +x ~/.local/bin/minikube
```

### Install helm

```
$ curl -sL https://get.helm.sh/helm-v3.4.1-linux-amd64.tar.gz -O \
    && tar -xzf helm-v3.4.1-linux-amd64.tar.gz linux-amd64/helm --strip-components=1 \
    && mv helm ~/.local/bin \
    && chmod +x ~/.local/bin/helm \
    && rm helm-v3.4.1-linux-amd64.tar.gz
```

## Operate

### Start minikube

```
$ minikube start

😄  minikube v1.14.2 en Ubuntu 20.04
✨  Automatically selected the docker driver
👍  Starting control plane node minikube in cluster minikube
🚜  Pulling base image ...
💾  Downloading Kubernetes v1.19.2 preload ...
    > preloaded-images-k8s-v6-v1.19.2-docker-overlay2-amd64.tar.lz4: 486.33 MiB
🔥  Creating docker container (CPUs=2, Memory=3900MB) ...
🐳  Preparando Kubernetes v1.19.2 en Docker 19.03.8...
🔎  Verifying Kubernetes components...
🌟  Enabled addons: storage-provisioner, default-storageclass
🏄  Done! kubectl is now configured to use "minikube" by default
```

## Deploy metrics server

```
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/download/v0.3.6/components.yaml
```

## Install prometheus

```
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm search repo prometheus-community
helm install prometheus prometheus-community/prometheus --create-namespace
```

## Connect to prometheus server

- Create tunnel

```
$ kubectl port-forward services/prometheus-server 8080:80
```

- Connect to endpoint

http://localhost:8080/metrics