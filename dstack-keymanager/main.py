import os
import socket
import hashlib
import requests

from eth_account import Account
from eth_account.messages import encode_defunct

from flask import Flask, Response, request
app = Flask(__name__)

def reverse_dns_lookup(ip_address):
    try:
        result = socket.gethostbyaddr(ip_address)
        return result[0]
    except socket.herror:
        return "unknown"

##########################
# Global Master key
##########################

# This will be set one of two ways:
# - By bootstrapping (just the first node)
# - By onboarding    (every other node)

# Key manager
xPriv = None


##########################
# Hardened per app subkeys
##########################

@app.route("/getkey")
def getkey():
    # Domain extension by hostname
    client_ip = request.remote_addr
    hostname = reverse_dns_lookup(client_ip).encode('utf-8')
    # TODO: replace with bip32 hardened key derivation
    appkey = hashlib.sha256(xPriv + hostname + xPriv).hexdigest()
    return appkey
    

##########################
# EVM-friendly Attestation
##########################

@app.route("/attest/<appdata>")
def attest(appdata):
    assert len(bytes.fromhex(appdata)) == 32
    # Domain extension by hostname
    client_ip = request.remote_addr
    hostname = reverse_dns_lookup(client_ip)
    newappdata = hashlib.sha256((appdata + hostname).encode('utf-8')).hexdigest()*2
    acct = Account.from_key(xPriv)
    sig = acct.sign_message(encode_defunct(hexstr=newappdata))
    return f"/attest/{appdata}: {sig.signature.hex()}"

#############################
# Bootstrap: Initialize xPriv
#############################

# This is to be called by the host
@app.route("/bootstrap")
def bootstrap():
    global xPriv
    if xPriv is not None: return "Already bootstrapped"
    # TODO: also return the quote
    
    xPriv = os.urandom(32)
    acct = Account.from_key(xPriv)
    appdata = hashlib.sha256(acct.address.encode('utf-8')).hexdigest()*2
    #appdata = 'cafebabe00000000000000000000000000000000000000000000000000000000'
    quote = requests.get(f"http://dstack-tee-services/attest/{appdata}").text
    return Response(f"Bootstrap key: {acct.address}\n \
    quote: {quote}", mimetype='text/plain')


########################
# Onboarding: TODO:
########################

# Verification for onboarding
def verify(quote, addr):
    # TODO onboarding
    
    # Need to construct the app data
    appdata = hashlib.sha256(addr)

    # Need to call the verification library, via subprocess if cli?
    # Or by http if another microservice


def check_i_am_allowed():
    # TODO: hardening and invalidating stale nodes
    
    # Use our local tcb info configuration to
    # determine if we are OK given the current configuration
    pass

# Transfer key
myPriv = None

@app.route("/register")
def register():
    # This produces an ephemeral encryption key
    return "/register"

# Hello 
@app.route("/")
def hello():
    return Response("keymanager", mimetype='text/plain')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5003)
