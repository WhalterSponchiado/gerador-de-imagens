from huggingface_hub import InferenceClient
from PIL import Image
from dotenv import load_dotenv
import os
import time
import json
from datetime import datetime

# Carrega variáveis do .env
load_dotenv()

TOKEN = os.getenv("HF_TOKEN")

if not TOKEN:
    raise ValueError("❌ Token não encontrado! Coloque HF_TOKEN no arquivo .env")

# Conecta ao modelo
client = InferenceClient(
    model="black-forest-labs/FLUX.1-schnell",
    token=TOKEN
)


# ===== FUNÇÃO PARA SALVAR HISTÓRICO =====
def salvar_historico(prompt, arquivo):

    registro = {
        "prompt": prompt,
        "arquivo": arquivo,
        "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    try:
        with open("historico.json", "r", encoding="utf-8") as f:
            dados = json.load(f)
    except:
        dados = []

    dados.append(registro)

    with open("historico.json", "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)


# ===== GERAR IMAGENS =====
def gerar_imagens(prompt, quantidade=4):

    os.makedirs("imagens", exist_ok=True)

    for i in range(quantidade):

        print(f"🎨 Gerando imagem {i+1}/{quantidade}...")

        try:
            imagem = client.text_to_image(prompt)

            nome_arquivo = f"imagens/imagem_{int(time.time())}_{i}.png"

            imagem.save(nome_arquivo)

            # salva no histórico
            salvar_historico(prompt, nome_arquivo)

            print(f"✅ Imagem salva em: {nome_arquivo}")

        except Exception as e:
            print("❌ Erro ao gerar imagem:", e)


# ===== PROGRAMA PRINCIPAL =====
def main():

    print("\n🧠 GERADOR DE IMAGENS COM IA")
    print("-" * 35)

    prompt = input("Digite o prompt da imagem: ")

    try:
        quantidade = int(input("Quantas imagens deseja gerar? "))
    except:
        quantidade = 4

    gerar_imagens(prompt, quantidade)

    print("\n🚀 Processo finalizado!")


if __name__ == "__main__":
    main()
