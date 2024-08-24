from flask import Flask
app = Flask(__name__)
import socket
print(socket.gethostname())

@app.route("/")
def hello():
    return "Hello from dstack simulated TEE service! hostname: " + socket.gethostname()

@app.route("/attest/{userdata}")
def attest(userdata):
    NotImplemented

@app.route("/attest/")
def attest_index():
    return "attestation! Try appending a 64-byte userdata"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)
