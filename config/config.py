
from pathlib import Path

# ==========================================
# DIRETÓRIO PRINCIPAL DO PROJETO
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent


# ==========================================
# MODELOS DE INTELIGÊNCIA ARTIFICIAL
# ==========================================

MODELO_CHAT = "qwen2.5:3b"

MODELO_EMBEDDING = "embeddinggemma"


# ==========================================
# CONFIGURAÇÕES DO CHATBOT
# ==========================================

TEMPERATURA = 0.2

QUANTIDADE_RESULTADOS = 5

TAMANHO_FRAGMENTO = 1200

SOBREPOSICAO_FRAGMENTO = 200

TAMANHO_LOTE_EMBEDDING = 32


# ==========================================
# DIRETÓRIOS DO PROJETO
# ==========================================

PASTA_DOCUMENTOS = BASE_DIR / "documentos"

PASTA_DATABASE = BASE_DIR / "database"

PASTA_CHROMA = PASTA_DATABASE / "chroma"

PASTA_MODULES = BASE_DIR / "modules"

PASTA_UTILS = BASE_DIR / "utils"


# ==========================================
# BANCO DE DADOS
# ==========================================

CAMINHO_FEEDBACK = PASTA_DATABASE / "feedback.db"

NOME_COLECAO = "documentos"


# ==========================================
# CONFIGURAÇÕES DOS DOCUMENTOS
# ==========================================

EXTENSOES_PERMITIDAS = [".pdf"]

TAMANHO_MINIMO_TEXTO = 30


# ==========================================
# INICIALIZAÇÃO DOS DIRETÓRIOS
# ==========================================

def inicializar_diretorios():

    diretorios = [
        PASTA_DOCUMENTOS,
        PASTA_DATABASE,
        PASTA_CHROMA,
        PASTA_MODULES,
        PASTA_UTILS
    ]

    for diretorio in diretorios:

        diretorio.mkdir(
            parents=True,
            exist_ok=True
        )


# ==========================================
# INICIALIZAÇÃO DO SISTEMA
# ==========================================

def inicializar_sistema():

    inicializar_diretorios()

    print("Sistema inicializado com sucesso!")

    print(f"Diretório principal: {BASE_DIR}")

    print(f"Modelo de chat: {MODELO_CHAT}")

    print(f"Modelo de embedding: {MODELO_EMBEDDING}")
