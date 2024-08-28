This is a minimalist key management service for pods in the Tstack.

It uses the Ethereum Goerli testnet as an on-chain registry.

## Interfaces
This provides a very small number of interfaces that pods in the container can access.

### Persistent key

`http://dstack-keymanager/sealkey`

This provides a sealing key. Further key derivation is up to you


### Ethereum-friendly attestation

Once the `dstack` instance is registered, you can use it to carry out nested attestation in an Ethereum-friendly way.

`dstack-keymanager/attest/<appdata>`

The resulting signature can be verified in Solidity using the contract:

`keymanager.verifyAttestation(hostname, appdata, sig)`

## How it works

### Contracts

A key manager contract on an EVM chain keeps track of:
- Allowed MRENCLAVEs
- Allowed TCB configurations

By default, this system is set up to use a shared instance on Goerli: TODO

To start your own network, it's necessary to launch a key manager contract.
Tools in this repo are provided to do this, but this doesn't doesn't have to happen from an enclave.

### Bootstrapping

As a host, you can ask the key manager to initialize the contract:

- `dstack-keymanager/bootstrap`

This produces a master secret key, the public key of which will be associated with the contract.

This produces a quote, which should be sent via "blob" data to a transaction.
This quote becomes part of the TCB, it's something auditors would need to validate.

Since the default Goerli instance is already bootstrapped, you'll have to run your own.

### Join your node to the network

When you (the host) first start your enclave, you need to join it to the network.
This requires providing a remote attestation of blob data along with the request.

- `dstack-keymanager/register`

If the session has not been established yet, generate a public key, request a copy of the master
secret encrypted to this public key.

Later when an encrypted key is obtained, either via a blob submitted in response,

- `dstack-keymanager/register/<enckey>`


### Help others onboard

Some existing registered enclave needs to reply to valid registrations by providing them an encrypted copy of the master secret.

The easiest way is using blobs.

- `dstack-keymanager/helper/<addr>`

 can be called by the host to produce an enckey for the newly joined node.
 This can be posted on-chain, along with an attestation.