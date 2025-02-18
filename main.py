from http.client import responses

import google.generativeai as genai
import os
from flask import Flask, request, jsonify

from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


def gerar_receita(mensagem_usuario):
    prompt = f"""
    Você é um nutricionista e fisiculturista que cria receitas fitness, proteicas e de baixa caloria. 
    Responda de maneira descontraída e motivacional, incentivando a alimentação saudável.

    O usuário pediu: {mensagem_usuario}

    Retorne a receita com:
    1. Nome do prato
    2. Ingredientes
    3. Modo de preparo detalhado
    4. Dicas nutricionais
        """

    model = genai.GenerativeModel("gemini-1.5-flash")

    response = model.generate_content(prompt)

    return response.text


@app.route("/gerar-receita", methods=["POST", "GET"])
def chat():
    if request.method == "GET":
        return jsonify({"mensagem": "Use uma requisicao "})

    dados = request.json
    mensagem_usuario = dados.get("mensagem")

    if not mensagem_usuario:
        return jsonify({"erro": "Por favor, envie uma mensagem válida."}), 400

    resposta = gerar_receita(mensagem_usuario)
    return jsonify({"resposta": resposta})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
