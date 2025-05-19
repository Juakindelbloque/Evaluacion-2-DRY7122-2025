from flask import Flask


sample = Flask(__name__)

@sample.route("/hola")
def hola():
    return "Hola Mundo programación de redes"


if __name__ == "__main__":
    sample.run(host="0.0.0.0", port=3000)
