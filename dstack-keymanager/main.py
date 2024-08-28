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

def ecdsa_sign(privkey, msg):
    return NotImplemented

@app.route("/")
def hello():
    return Response("keymanager", mimetype='text/plain')

# Key manager
xPriv = None

# Verification
def verify(quote, addr):
    # Need to construct the app data
    appdata = hashlib.sha256(addr)

    # It was computed w

@app.route("/bootstrap")
def bootstrap():
    global xPriv
    if xPriv is None:
        xPriv = os.urandom(32)
    acct = Account.from_key(xPriv)
    #appdata = hashlib.sha256(acct.address.encode('utf-8')).hexdigest()+32*'00'
    appdata = 'cafebabe00000000000000000000000000000000000000000000000000000000'
    quote = requests.get(f"http://dstack-tee-services/attest/{appdata}").text
    return Response(f"Bootstrap key: {acct.address}\n \
    quote: {quote}", mimetype='text/plain')

def check_i_am_allowed():
    # Use our local tcb info configuration to
    # determine if we are OK given the current configuration
    pass

# Transfer key
myPriv = None

@app.route("/register")
def register():
    # This produces an ephemeral encryption key
    return "/register"

@app.route("/attest/<appdata>")
def attest(appdata):
    assert len(bytes.fromhex(appdata)) == 32
    # Domain extension by hostname
    client_ip = request.remote_addr
    hostname = reverse_dns_lookup(client_ip)
    newappdata = hashlib.sha256((hostname + appdata).encode('utf-8')).hexdigest()*2
    return f"/attest/{appdata}"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5003)
