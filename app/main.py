from flask import Flask
app = Flask(__name__)
import socket
print(socket.gethostname())

@app.route("/")
def hello():
    return "Hello from dstack-app!\nhostname: " + socket.gethostname()

if __name__ == "__main__":
    app.run(host='0.0.0.0')
