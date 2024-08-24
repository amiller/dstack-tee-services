from flask import Flask
app = Flask(__name__)
import socket
print(socket.gethostname())
from urllib.request import urlopen, Request

def get_mock_attestation(appdata):
    url = f"https://dcap-dummy.sirrah.suave.flashbots.net/dcap/{appdata}"
    req = Request(url, headers={'User-Agent' : "Magic Browser"})
    obj = urlopen(req).read().decode('utf-8')
    return obj + '\n'


@app.route("/")
def hello():
    return "Hello from dstack simulated TEE service! hostname: " + socket.gethostname()

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
