
import chromadb

from config.config import (
    PASTA_CHROMA,
    NOME_COLECAO
)


# ==========================================
# CLIENTE CHROMADB
# ==========================================

client = chromadb.PersistentClient(
    path=str(PASTA_CHROMA)
)


# ==========================================
# OBTER OU CRIAR COLEÇÃO
# ==========================================

def obter_colecao():

    return client.get_or_create_collection(
        name=NOME_COLECAO,
        metadata={
            "hnsw:space": "cosine"
        }
    )


# ==========================================
# VERIFICAR SE DOCUMENTO JÁ FOI INDEXADO
# ==========================================

def documento_ja_indexado(nome, hash_documento):

    try:

        colecao = obter_colecao()

        resultado = colecao.get(
            where={"arquivo": nome},
            include=["metadatas"]
        )

        metadados = resultado["metadatas"]

        if not metadados:
            return False

        return all(
            meta.get("hash_documento") == hash_documento
            for meta in metadados
        )

    except Exception:
        return False


# ==========================================
# ADICIONAR DOCUMENTOS
# ==========================================

def adicionar_fragmentos(
    fragmentos,
    embeddings,
    identificadores
):

    if not fragmentos:
        return 0

    if not (
        len(fragmentos)
        == len(embeddings)
        == len(identificadores)
    ):
        raise ValueError(
            "A quantidade de fragmentos, embeddings "
            "e identificadores precisa ser igual."
        )

    colecao = obter_colecao()

    documentos = [
        item["texto"]
        for item in fragmentos
    ]

    metadados = [
        {
            "arquivo": item["arquivo"],
            "pagina": item["pagina"],
            "fragmento": item["fragmento"],
            "hash_documento": item["hash_documento"]
        }
        for item in fragmentos
    ]

    colecao.add(
        ids=identificadores,
        documents=documentos,
        embeddings=embeddings,
        metadatas=metadados
    )

    return len(fragmentos)


# ==========================================
# REMOVER DOCUMENTO INDEXADO
# ==========================================

def remover_documento_indexado(nome):

    try:

        colecao = client.get_collection(
            name=NOME_COLECAO
        )

        colecao.delete(
            where={
                "arquivo": nome
            }
        )

    except Exception as erro:

        if "does not exist" in str(erro).lower():
            return

        raise


# ==========================================
# CONTAR FRAGMENTOS
# ==========================================

def contar_fragmentos():

    try:

        colecao = obter_colecao()

        return colecao.count()

    except Exception:
        return 0


# ==========================================
# LISTAR DOCUMENTOS INDEXADOS
# ==========================================

def listar_documentos_indexados():

    colecao = obter_colecao()

    resultado = colecao.get(
        include=["metadatas"]
    )

    documentos = set()

    for metadado in resultado["metadatas"]:

        if metadado and "arquivo" in metadado:
            documentos.add(metadado["arquivo"])

    return sorted(documentos)
