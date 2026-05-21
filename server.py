from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

@app.route("/api/dados", methods=["POST"])
def receber_dados():
    data = request.json
    print(" Recebido:", data)

    agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open("dados.csv", "a") as f:
        f.write(f"{agora},{data.get('temperatura')}\n")

    return jsonify({"status": "ok"}), 200

@app.route("/")
def home():
    return "Servidor rodando "
