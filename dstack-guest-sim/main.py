from flask import Flask, Response, request
app = Flask(__name__)
import socket
print(socket.gethostname())
from urllib.request import urlopen, Request
import subprocess
import pydig
import hashlib

def reverse_dns_lookup(ip_address):
    try:
        result = socket.gethostbyaddr(ip_address)
        return result[0]
    except socket.herror:
        return "Unable to perform reverse DNS lookup"

def get_mock_attestation(appdata):
    url = f"http://ns31695324.ip-141-94-163.eu:10080/attestation/{appdata}"
    req = Request(url, headers={'User-Agent' : "Magic Browser"})
    obj = urlopen(req).read().hex()
    return obj + '\n'

@app.route("/")
def hello():
    client_ip = request.remote_addr
    def generate():
        yield "Hello, from dstack simulated TEE service! \n"
        yield "hostname: " + socket.gethostname() + '\n'
        yield f"Your IP address is: {client_ip}" + '\n'
        hostname = reverse_dns_lookup(client_ip)
        yield f"PTR record for {client_ip}: {hostname}"

    return Response(generate(), mimetype='text/plain')

@app.route("/what/ip")
def whatismyip():
    return request.remote_addr

@app.route("/what/hostname")
def whatismyhostname():
    return reverse_dns_lookup(request.remote_addr)

@app.route("/attest/<appdata>")
def attest(appdata):
    assert len(bytes.fromhex(appdata)) == 32
    # Domain extension by hostname
    client_ip = request.remote_addr
    hostname = reverse_dns_lookup(client_ip)
    newappdata = hashlib.sha256((hostname + appdata).encode('utf-8')).hexdigest()*2
    return get_mock_attestation(newappdata)

@app.route("/attest/")
def attest_index():
    return "attestation! Try appending a 32-byte userdata " + \
        " attest/cafebabe00000000000000000000000000000000000000000000000000000000"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)
