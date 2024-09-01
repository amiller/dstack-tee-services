#!/bin/bash

# This script should be called by the host.
# It does not need to run in the enclave

# TODO: Finish this actual deployment script


PRIVATE_KEY=$(cat privkey)

# Deploy the contract
pushd contracts
CONTRACT=$(forge deploy KeyManager.sol:KeyManager)
popd

# Execute bootstrap
curl http://192.168.49.2:31771/bootstrap > out
# parse out into addr, quote
ADDR=$(cat out | grep 0x)

# Store quote for later

# Post the key on-chain
cast call $CONTRACT "bootstrap" $ADDR

