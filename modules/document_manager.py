
from pathlib import Path

from config.config import (
    PASTA_DOCUMENTOS,
    EXTENSOES_PERMITIDAS
)


# ==========================================
# LISTAR DOCUMENTOS
# ==========================================

def listar_documentos():

    PASTA_DOCUMENTOS.mkdir(
        parents=True,
        exist_ok=True
    )

    arquivos = [
        arquivo
        for arquivo in PASTA_DOCUMENTOS.iterdir()
        if arquivo.is_file()
        and arquivo.suffix.lower() in EXTENSOES_PERMITIDAS
    ]

    return sorted(
        arquivos,
        key=lambda arquivo: arquivo.name.lower()
    )


# ==========================================
# VALIDAR ARQUIVO ENVIADO
# ==========================================

def validar_arquivo(arquivo):

    nome = Path(arquivo.name).name

    if Path(nome).suffix.lower() not in EXTENSOES_PERMITIDAS:
        raise ValueError(
            f"O arquivo {nome} não é um PDF válido."
        )

    conteudo = arquivo.getvalue()

    if not conteudo:
        raise ValueError(
            f"O arquivo {nome} está vazio."
        )

    if not conteudo.startswith(b"%PDF-"):
        raise ValueError(
            f"O arquivo {nome} não possui uma assinatura PDF válida."
        )

    return nome, conteudo


# ==========================================
# GERAR NOME DISPONÍVEL
# ==========================================

def gerar_nome_disponivel(nome):

    caminho = PASTA_DOCUMENTOS / nome

    if not caminho.exists():
        return nome

    contador = 1

    while True:

        novo_nome = (
            f"{Path(nome).stem}_{contador}"
            f"{Path(nome).suffix}"
        )

        novo_caminho = PASTA_DOCUMENTOS / novo_nome

        if not novo_caminho.exists():
            return novo_nome

        contador += 1


# ==========================================
# ADICIONAR DOCUMENTO
# ==========================================

def adicionar_documento(arquivo):

    PASTA_DOCUMENTOS.mkdir(
        parents=True,
        exist_ok=True
    )

    nome, conteudo = validar_arquivo(arquivo)

    caminho_original = PASTA_DOCUMENTOS / nome

    # Verificar se o mesmo documento já existe

    if caminho_original.exists():

        if caminho_original.read_bytes() == conteudo:

            return {
                "sucesso": True,
                "duplicado": True,
                "nome": nome,
                "mensagem": "Este documento já está cadastrado."
            }

    # Criar nome disponível

    nome_final = gerar_nome_disponivel(nome)

    caminho_final = PASTA_DOCUMENTOS / nome_final

    # Salvar documento

    caminho_final.write_bytes(conteudo)

    return {
        "sucesso": True,
        "duplicado": False,
        "nome": nome_final,
        "mensagem": "Documento adicionado com sucesso."
    }


# ==========================================
# EXCLUIR DOCUMENTO
# ==========================================

def excluir_documento(nome):

    nome = Path(nome).name

    if Path(nome).suffix.lower() not in EXTENSOES_PERMITIDAS:
        raise ValueError("Documento inválido.")

    caminho = PASTA_DOCUMENTOS / nome

    if not caminho.exists() or not caminho.is_file():
        raise FileNotFoundError(
            f"Documento não encontrado: {nome}"
        )

    # Remover os fragmentos do banco vetorial

    from modules.vector_database import (
        remover_documento_indexado
    )

    remover_documento_indexado(nome)

    # Remover arquivo físico

    caminho.unlink()

    return True

# ==========================================
# CONTAR DOCUMENTOS
# ==========================================

def contar_documentos():

    return len(listar_documentos())


# ==========================================
# OBTER INFORMAÇÕES DOS DOCUMENTOS
# ==========================================

def informacoes_documentos():

    arquivos = listar_documentos()

    informacoes = []

    for arquivo in arquivos:

        informacoes.append({
            "nome": arquivo.name,
            "tamanho": arquivo.stat().st_size,
            "caminho": arquivo
        })

    return informacoes
