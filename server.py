from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

#  banco em memória
dados = []

#  RECEBER DADOS
@app.route("/api/teste", methods=["POST"])
def receber_dados():
    data = request.json

    agora = datetime.now().strftime("%H:%M:%S")

    registro = {
        "tempo": agora,
        "temperatura": data.get("temperatura")
    }

    dados.append(registro)

    # limitar histórico
    if len(dados) > 50:
        dados.pop(0)

    print(" ", registro)

    return jsonify({"status": "ok"}), 200


#  RETORNAR DADOS
@app.route("/dados")
def obter_dados():
    return jsonify(dados)


#  GRÁFICO EM TEMPO REAL
@app.route("/grafico")
def grafico():
    return """
<!DOCTYPE html>
<html>
<head>
<title>Temperatura ESP32</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body>

<h2>🌡 Temperatura em Tempo Real</h2>
<canvas id="grafico"></canvas>

<script>

let chart;

async function atualizar() {

    const resp = await fetch('/dados');
    const data = await resp.json();

    const labels = data.map(d => d.tempo);
    const valores = data.map(d => d.temperatura);

    if (!chart) {
        chart = new Chart(document.getElementById("grafico"), {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Temperatura (°C)',
                    data: valores,
                    borderColor: 'red',
                    borderWidth: 2
                }]
            }
        });
    } else {
        chart.data.labels = labels;
        chart.data.datasets[0].data = valores;
        chart.update();
    }
}

setInterval(atualizar, 5000);
atualizar();

</script>

</body>
</html>
"""


#  HOME
@app.route("/")
def home():
    return "Servidor online "
