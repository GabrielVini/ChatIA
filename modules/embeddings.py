
import ollama

from config.config import (
    MODELO_EMBEDDING,
    TAMANHO_LOTE_EMBEDDING
)


# ==========================================
# GERAR EMBEDDINGS
# ==========================================

def gerar_embeddings(textos):

    if not textos:
        return []

    embeddings = []

    for inicio in range(
        0,
        len(textos),
        TAMANHO_LOTE_EMBEDDING
    ):

        fim = inicio + TAMANHO_LOTE_EMBEDDING

        lote = textos[inicio:fim]

        resultado = ollama.embed(
            model=MODELO_EMBEDDING,
            input=lote
        )

        vetores = resultado["embeddings"]

        if len(vetores) != len(lote):
            raise RuntimeError(
                "A quantidade de embeddings retornada "
                "não corresponde à quantidade de textos."
            )

        embeddings.extend(vetores)

    return embeddings


# ==========================================
# GERAR EMBEDDING DE UMA PERGUNTA
# ==========================================

def gerar_embedding_pergunta(pergunta):

    if not pergunta or not pergunta.strip():
        raise ValueError("A pergunta não pode estar vazia.")

    resultado = ollama.embed(
        model=MODELO_EMBEDDING,
        input=pergunta
    )

    return resultado["embeddings"][0]
