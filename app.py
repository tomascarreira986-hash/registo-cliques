from flask import Flask, render_template, jsonify, Response
import sqlite3
from datetime import datetime

app = Flask(__name__)
DB_NAME = "cliques.db"


def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def criar_tabela():
    conn = get_db_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS cliques (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            botao TEXT NOT NULL,
            numero INTEGER NOT NULL,
            data TEXT NOT NULL,
            hora TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/click/<botao>")
def click(botao):
    conn = get_db_connection()

    hoje = datetime.now().strftime("%Y-%m-%d")
    hora = datetime.now().strftime("%H:%M")

    total_hoje = conn.execute(
        "SELECT COUNT(*) FROM cliques WHERE data = ?", (hoje,)
    ).fetchone()[0]

    numero = total_hoje + 1

    conn.execute(
        "INSERT INTO cliques (botao, numero, data, hora) VALUES (?, ?, ?, ?)",
        (botao, numero, hoje, hora)
    )
    conn.commit()

    dias = conn.execute("""
        SELECT data, COUNT(*) as total
        FROM cliques
        GROUP BY data
        ORDER BY data DESC
    """).fetchall()

    conn.close()

    lista_dias = [{"data": d["data"], "total": d["total"]} for d in dias]

    return jsonify({
        "numero": numero,
        "data": hoje,
        "hora": hora,
        "dias": lista_dias
    })


@app.route("/download")
def download():
    conn = get_db_connection()

    registos = conn.execute("""
        SELECT data, hora, botao, numero
        FROM cliques
        ORDER BY data, numero
    """).fetchall()

    conn.close()

    texto = "RELATÓRIO DE CLIQUES\n"
    texto += "=====================\n\n"

    data_atual = ""

    for r in registos:
        if r["data"] != data_atual:
            data_atual = r["data"]
            texto += f"\nData: {data_atual}\n"
            texto += "-" * 30 + "\n"

        texto += f"Nº {r['numero']} | Hora: {r['hora']} | Atividade: {r['botao']}\n"

    return Response(
        texto,
        mimetype="text/plain",
        headers={"Content-Disposition": "attachment;filename=relatorio_cliques.txt"}
    )


if __name__ == "__main__":
    criar_tabela()
    app.run(host="0.0.0.0", port=3000, debug=True)
