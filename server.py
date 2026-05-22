from flask import Flask, request, jsonify
from datetime import datetime
import sqlite3

app = Flask(__name__)

#  CRIAR BANCO
def init_db():
    conn = sqlite3.connect("dados.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS temperatura (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            valor REAL
        )
    """)
    conn.commit()
    conn.close()

init_db()

# ==========================
# RECEBER DADOS
# ==========================
@app.route("/api/teste", methods=["POST"])
def receber_dados():
    data = request.json

    temp = data.get("temperatura")
    agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = sqlite3.connect("dados.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO temperatura (timestamp, valor) VALUES (?, ?)",
                   (agora, temp))
    conn.commit()
    conn.close()

    print(" ", temp)

    return jsonify({"status": "ok"})


# ==========================
# RETORNAR DADOS
# ==========================
@app.route("/dados")
def dados():
    conn = sqlite3.connect("dados.db")
    cursor = conn.cursor()

    cursor.execute("SELECT timestamp, valor FROM temperatura ORDER BY id DESC LIMIT 50")
    rows = cursor.fetchall()

    conn.close()

    data = [{"tempo": r[0], "temperatura": r[1]} for r in reversed(rows)]
    return jsonify(data)


# ==========================
# DASHBOARD WEB
# ==========================
@app.route("/grafico")
def grafico():
    return """
<!DOCTYPE html>
<html>
<head>
<title>Dashboard IoT</title>
https://cdn.jsdelivr.net/npm/chart.jsscript>
</head>
<body>

<h2>🌡 Monitoramento de Temperatura</h2>
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
                    borderColor: 'blue',
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


@app.route("/")
def home():
    return "Servidor IoT rodando ✅"
