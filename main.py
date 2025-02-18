import google.generativeai as genai
import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv

# Carrega as variáveis de ambiente
load_dotenv()

app = Flask(__name__)

# Configura a API Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


def gerar_receita(mensagem_usuario):
    """Gera uma receita formatada usando a API Gemini."""
    prompt = f"""
    Você é um nutricionista e fisiculturista que cria receitas fitness, proteicas e de baixa caloria. 
    Responda de maneira descontraída e motivacional, incentivando a alimentação saudável.

    O usuário pediu: {mensagem_usuario}

    Retorne a receita com esse formato exato:

    Nome do Prato: [Nome da receita]

    Introdução: [Breve descrição da receita]

    Ingredientes:
    - [Ingrediente 1]
    - [Ingrediente 2]
    - [Ingrediente 3]

    Modo de Preparo:
    1. [Passo 1]
    2. [Passo 2]
    3. [Passo 3]

    Dicas Nutricionais:
    - [Dica 1]
    - [Dica 2]
    """

    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)

    # Captura a resposta e formata em JSON
    receita = response.text.split("\n\n")

    # Estrutura padrão para resposta formatada
    receita_formatada = {
        "mensagem": "",  # Mensagem personalizada
        "introducao": "",
        "nome_prato": "",
        "ingredientes": [],
        "modo_preparo": [],
        "dicas_nutricionais": []
    }

    for bloco in receita:
        if bloco.startswith("Nome do Prato:"):
            receita_formatada["nome_prato"] = bloco.replace("Nome do Prato:", "").strip()
        elif bloco.startswith("Introdução:"):
            receita_formatada["introducao"] = bloco.replace("Introdução:", "").strip()
        elif bloco.startswith("Ingredientes:"):
            receita_formatada["ingredientes"] = [item.strip("- ") for item in bloco.split("\n")[1:]]
        elif bloco.startswith("Modo de Preparo:"):
            receita_formatada["modo_preparo"] = [item.strip("0123456789. ") for item in bloco.split("\n")[1:]]
        elif bloco.startswith("Dicas Nutricionais:"):
            receita_formatada["dicas_nutricionais"] = [item.strip("- ") for item in bloco.split("\n")[1:]]

    # Adiciona uma mensagem personalizada usando o nome da receita
    receita_formatada["mensagem"] = f"Oii! Aqui está sua receita de {receita_formatada['nome_prato']}! 😋"

    return receita_formatada


@app.route("/gerar-receita", methods=["POST", "GET"])
def chat():
    """Rota para geração de receitas."""
    if request.method == "GET":
        return jsonify({"mensagem": "Use uma requisição POST para enviar uma mensagem válida."})

    dados = request.json
    mensagem_usuario = dados.get("mensagem")

    if not mensagem_usuario:
        return jsonify({"erro": "Por favor, envie uma mensagem válida."}), 400

    resposta = gerar_receita(mensagem_usuario)
    return jsonify(resposta)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
