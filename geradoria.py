from huggingface_hub import InferenceClient
from PIL import Image
import os
import time
from dotenv import load_dotenv

# Carrega variáveis do arquivo .env
load_dotenv()

# Pega o token da variável de ambiente
TOKEN = os.getenv("HF_TOKEN")

if not TOKEN:
    raise ValueError("❌ Token não encontrado! Coloque HF_TOKEN no arquivo .env")

# Conecta ao modelo
client = InferenceClient(
    model="black-forest-labs/FLUX.1-schnell",
    token=TOKEN
)

print("🧠 Iniciando a geração da imagem...")

try:
    # Prompt da imagem
    prompt = "Cachorro fumando um charuto estilo cinematográfico"

    # Gera a imagem
    image = client.text_to_image(prompt)

    # Nome do arquivo
    filename = "resultado_final.png"

    # Salva a imagem
    image.save(filename)

    print(f"✅ Sucesso! Imagem salva como {filename}")

except Exception as e:
    # erro comum quando o modelo ainda está carregando
    if "503" in str(e) or "loading" in str(e).lower():
        print("⚠️ O modelo está carregando nos servidores...")
        print("⏳ Aguarde 20 segundos e execute novamente.")
        time.sleep(20)
    else:
        print(f"❌ Erro inesperado: {e}")
