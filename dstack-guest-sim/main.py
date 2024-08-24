from flask import Flask, Response, request
app = Flask(__name__)
import socket
print(socket.gethostname())
from urllib.request import urlopen, Request
import subprocess
import pydig

def reverse_dns_lookup(ip_address):
    try:
        result = socket.gethostbyaddr(ip_address)
        return result[0]
    except socket.herror:
        return "Unable to perform reverse DNS lookup"

def get_mock_attestation(appdata):
    url = f"https://dcap-dummy.sirrah.suave.flashbots.net/dcap/{appdata}"
    req = Request(url, headers={'User-Agent' : "Magic Browser"})
    obj = urlopen(req).read().decode('utf-8')
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

@app.route("/attest/<appdata>")
def attest(appdata):
    assert len(bytes.fromhex(appdata)) == 64
    return get_mock_attestation(appdata)

@app.route("/attest/")
def attest_index():
    return "attestation! Try appending a 64-byte userdata " + \
        " attest/cafebabe000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)
