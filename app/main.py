from flask import Flask, Response
app = Flask(__name__)

import socket
import subprocess

def latest():
    cmd = "cast block-number --flashbots"
    return subprocess.check_output(cmd, shell=True).decode('utf-8')


@app.route("/")
def hello():
    def generate():
        yield "Hello from dstack-app!\n"
        yield "hostname: " + socket.gethostname() + "\n"
        yield "cast block latest:" + latest()

    return Response(generate(), mimetype='text/plain')

if __name__ == "__main__":
    app.run(host='0.0.0.0')
