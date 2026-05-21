from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

#  banco de dados em memória
dados = []

# -------------------------
# RECEBER DADOS DO ESP32
# -------------------------
@app.route("/api/dados", methods=["POST"])
def receber_dados():
    data = request.json

    agora = datetime.now().strftime("%H:%M:%S")

    registro = {
        "tempo": agora,
        "temperatura": data.get("temperatura")
    }

    dados.append(registro)

    # manter só últimos 50 pontos
    if len(dados) > 50:
        dados.pop(0)

    print(" ", registro)

    return jsonify({"status": "ok"}), 200


# -------------------------
# RETORNAR DADOS (API)
# -------------------------
@app.route("/dados")
def obter_dados():
    return jsonify(dados)


# -------------------------
# GRÁFICO EM TEMPO REAL
# -------------------------
@app.route("/grafico")
def grafico():
    return """
<!DOCTYPE html>
<html>
<head>
    <title>Temperatura em Tempo Real</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body>

<h2>🌡 Temperatura ESP32 (Tempo Real)</h2>

<canvas id="grafico"></canvas>

<script>
let chart;

async function carregarDados() {
    const resp = await fetch('/dados');
    const dados = await resp.json();

    const labels = dados.map(d => d.tempo);
    const valores = dados.map(d => d.temperatura);

    if (chart) {
        chart.data.labels = labels;
        chart.data.datasets[0].data = valores;
        chart.update();
    } else {
        chart = new Chart(document.getElementById("grafico"), {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Temperatura (°C)',
                    data: valores,
                    borderWidth: 2,
                    borderColor: 'red'
                }]
            }
        });
    }
}

//  atualiza a cada 5 segundos
setInterval(carregarDados, 5000);

// carrega na inicialização
carregarDados();
</script>

</body>
</html>
"""


# -------------------------
# HOME
# -------------------------
@app.route("/")
def home():
    return "Servidor online "
