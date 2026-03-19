from flask import Flask, render_template, request
from gerador import gerar_imagens
import os
import json

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():

    imagem = None
    historico = []

    if request.method == "POST":

        prompt = request.form["prompt"]
        gerar_imagens(prompt, 1)

        pasta = "imagens"
        arquivos = sorted(os.listdir(pasta), reverse=True)

        if arquivos:
            imagem = f"imagens/{arquivos[0]}"

    # carregar histórico
    if os.path.exists("historico.json"):
        with open("historico.json", "r", encoding="utf-8") as f:
            historico = json.load(f)

    # galeria
    galeria = []
    if os.path.exists("imagens"):
        galeria = os.listdir("imagens")

    return render_template(
        "index.html",
        imagem=imagem,
        historico=historico,
        galeria=galeria
    )


if __name__ == "__main__":
    app.run(debug=True)


#projeto futuro colocar em web