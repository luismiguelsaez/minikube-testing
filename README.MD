
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

### Deploy metrics server

```
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/download/v0.3.6/components.yaml
```

### Install prometheus

```
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm search repo prometheus-community
helm install prometheus prometheus-community/prometheus --create-namespace
```

### Connect to prometheus server

- Create tunnel

```
$ kubectl port-forward services/prometheus-server 8080:80
```

- Connect to endpoint

http://localhost:8080/metrics


## Applications deployment

### Build example application image

```
docker build -t app:latest app
docker tag app:latest luismiguelsaez/rest-test:latest
docker login -u luismiguelsaez
docker push luismiguelsaez/rest-test:latest
```

### Deploy traefik2

```
kubectl apply -f k8s/traefik2
```

### Deploy application

```
kubectl apply -f k8s/app
```

### Access traefik admin and web endpoints

```
kubectl port-forward services/traefik 8080:8080 8000:8000
```

- Admin dashboard

http://localhost:8080

- Application routing test

```
$ curl -H"Host:app1.traefik.io" http://localhost:8000 -w"%{http_code} %{time_connect}/%{time_total}\n"
"Hello World, I'm application 1 and my container is: app1-deployment-7d774897c5-s29zn 2020-11-13 12:04:37.953583"
200 0,001142/0,022243

$ curl -H"Host:app2.traefik.io" http://localhost:8000 -w"%{http_code} %{time_connect}/%{time_total}\n"
"Hello World, I'm application 2 and my container is: app2-deployment-cbf9cbfb9-c8g6m 2020-11-13 12:04:50.666509"
200 0,000491/0,012286
```