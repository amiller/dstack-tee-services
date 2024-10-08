# Sample kubernetes environment with minimal support for remote attestation

`deployment-sim.yaml`:

 This sets up two deployments, the `app` and the `guest services`.
 Here the guest services is instantiated using a mock remote attestation environment.

## Remote attestation interface

This provides a single feature:

- `/attest/{appdata}`
  The single argument `appdata` should be 32 bytes of hex encoded data

  This returns a quote appropriate for the enclave environment it's running in.

  This can be a dummy attestation where the appdata comes from an external source.

In particular look at `app/main.py` for how it's used:
  ```python
        appdata = 'cafebabe00000000000000000000000000000000000000000000000000000000'
        url = f"http://dstack-tee-services/attest/{appdata}"  
  ```

and in `dstack-guest-sim/main.py` for how it can be simulated through a remote dummy fetch:
```python
    url = f"https://dcap-dummy.sirrah.suave.flashbots.net/dcap/{appdata}"
    req = Request(url, headers={'User-Agent' : "Magic Browser"})
    obj = urlopen(req).read().decode('utf-8')
```

- A corresponding verifier remains TODO. This would simply consist of carrying forward the domain separation.

### Requirements

- minikube

It's necessary to run `eval $(minikube docker-env)` and then `build.sh` in order 

### Build and run instructions

Run `bash build.sh`, which is just the following:
```
docker build -t dstack-app:latest app
docker build -t dstack-guest-sim:latest dstack-guest-sim
minikube kubectl -- apply -f deployment-sim.yaml
```

then to load the locally mapped api endpoints in a browser:
```
minikube service --all
```

### next steps:
- Instantiate this with a proper TDX backend
- Include verification example