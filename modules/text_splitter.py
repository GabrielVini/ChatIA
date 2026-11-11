
from config.config import (
    TAMANHO_FRAGMENTO,
    SOBREPOSICAO_FRAGMENTO
)


# ==========================================
# DIVIDIR TEXTO EM FRAGMENTOS
# ==========================================

def dividir_texto(
    texto,
    tamanho=TAMANHO_FRAGMENTO,
    sobreposicao=SOBREPOSICAO_FRAGMENTO
):

    if tamanho <= 0:
        raise ValueError("O tamanho do fragmento deve ser positivo.")

    if sobreposicao < 0 or sobreposicao >= tamanho:
        raise ValueError(
            "A sobreposição deve ser menor que o tamanho do fragmento."
        )

    paragrafos = [
        paragrafo.strip()
        for paragrafo in texto.splitlines()
        if paragrafo.strip()
    ]

    palavras = []

    for paragrafo in paragrafos:
        palavras.extend(paragrafo.split())

    fragmentos = []

    inicio = 0
    passo = tamanho - sobreposicao

    while inicio < len(palavras):

        fim = inicio + tamanho

        trecho = " ".join(palavras[inicio:fim])

        if len(trecho.strip()) > 30:
            fragmentos.append(trecho)

        inicio += passo

    return fragmentos


# ==========================================
# PROCESSAR PÁGINAS EXTRAÍDAS DOS PDFS
# ==========================================

def processar_paginas(paginas):

    fragmentos = []

    for pagina in paginas:

        textos = dividir_texto(
            pagina["texto"]
        )

        for indice, texto in enumerate(textos):

            fragmentos.append({
                "texto": texto,
                "arquivo": pagina["arquivo"],
                "pagina": pagina["pagina"],
                "fragmento": indice
            })

    return fragmentos
