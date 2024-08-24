set -x
docker build -t dstack-app:latest app
docker build -t dstack-guest-sim:latest dstack-guest-sim
minikube kubectl -- delete deployment --all
minikube kubectl -- apply -f deployment-sim.yaml

