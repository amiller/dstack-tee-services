# Sample kubernetes environment with minimal support for remote attestation

`deployment-sim.yaml`:

 This sets up two deployments, the `app` and the `guest services` instantiated using a simuator.

### Requirements

- minikube

### Build and run instructions

```
docker build -t dstack-app:latest app
docker build -t dstack-guest-sim:latest dstack-guest-sim
minikube kubectl -- apply -f deployment-sim.yaml
```
