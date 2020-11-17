
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

### Deploy kubernetes dashboard

```
kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v2.0.0/aio/deploy/recommended.yaml
kubectl port-forward services/kubernetes-dashboard 8443:443 -n kubernetes-dashboard
```

https://localhost:8443

### Install prometheus + grafana

```
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo add stable https://charts.helm.sh/stable
helm repo update
helm install prometheus prometheus-community/kube-prometheus-stack
```

### Connect to prometheus and grafana servers

- Create tunnels

```
kubectl port-forward services/prometheus-kube-prometheus-prometheus 9090 2>&1 >/dev/null &
kubectl port-forward services/prometheus-grafana 8080:80 2>&1 >/dev/null &
```

- Connect to endpoints

http://localhost:9090/metrics
http://localhost:8080

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

## Deploy MongoDB

### Deploy service

```
kubectl apply -f k8s/mongodb
```

### Deploy exporter ( https://prometheus.io/docs/instrumenting/exporters/ )

- Add community repo ( https://github.com/prometheus-community/helm-charts/tree/main/charts/prometheus-mongodb-exporter )

```
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
```

- Get chart available values
```
helm show values prometheus-community/prometheus-mongodb-exporter
```

- Install chart
```
helm install mongodb-exporter prometheus-community/prometheus-mongodb-exporter -f k8s/mongodb/exporter-values.yml
```

- Check deployed components
```
kubectl get svc | grep mongodb-exporter
mongodb-exporter-prometheus-mongodb-exporter   ClusterIP   10.96.138.161    <none>        9216/TCP                        98s

kubectl get pod | grep mongodb-exporter
mongodb-exporter-prometheus-mongodb-exporter-6f546b47b7-q48p7   1/1     Running             0          103s

kubectl get servicemonitor | grep mongodb-exporter
mongodb-exporter-prometheus-mongodb-exporter         109s
```

- Check exported metrics
```
kubectl port-forward services/mongodb-exporter-prometheus-mongodb-exporter 9216 2>&1 >/dev/null &
```

http://localhost:9216/metrics

- Check prometheus mongodb target

http://127.0.0.1:9090/targets

## Stop minikube

```
$ minikube stop

✋  Stopping node "minikube"  ...
🛑  Apagando "minikube" mediante SSH...
🛑  1 nodes stopped.
```
