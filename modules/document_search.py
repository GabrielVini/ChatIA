
from modules.embeddings import gerar_embedding_pergunta

from modules.vector_database import obter_colecao

from config.config import QUANTIDADE_RESULTADOS


# ==========================================
# PESQUISAR DOCUMENTOS
# ==========================================

def pesquisar_documentos(pergunta):

    if not pergunta or not pergunta.strip():
        raise ValueError("Digite uma pergunta.")

    colecao = obter_colecao()

    quantidade = colecao.count()

    if quantidade == 0:
        raise ValueError(
            "Nenhum documento foi indexado. "
            "Adicione e processe um PDF primeiro."
        )

    # Gerar embedding da pergunta

    embedding = gerar_embedding_pergunta(
        pergunta
    )

    # Definir quantidade de resultados

    limite = min(
        QUANTIDADE_RESULTADOS,
        quantidade
    )

    # Pesquisar no ChromaDB

    resultado = colecao.query(
        query_embeddings=[embedding],
        n_results=limite,
        include=[
            "documents",
            "metadatas",
            "distances"
        ]
    )

    documentos = resultado["documents"][0]
    metadados = resultado["metadatas"][0]
    distancias = resultado["distances"][0]

    trechos = []

    for texto, metadata, distancia in zip(
        documentos,
        metadados,
        distancias
    ):

        trechos.append({
            "texto": texto,
            "arquivo": metadata["arquivo"],
            "pagina": metadata["pagina"],
            "distancia": distancia
        })

    return trechos
