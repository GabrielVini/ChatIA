
import hashlib

from modules.pdf_reader import extrair_texto_pdf

from modules.text_splitter import processar_paginas

from modules.embeddings import gerar_embeddings

from modules.vector_database import (
    adicionar_fragmentos,
    remover_documento_indexado,
    documento_ja_indexado
)


# ==========================================
# GERAR IDENTIFICADORES ÚNICOS
# ==========================================

def gerar_identificadores(fragmentos, hash_documento):

    identificadores = []

    for item in fragmentos:

        identificador = (
            f"{item['arquivo']}:"
            f"{hash_documento}:"
            f"{item['pagina']}:"
            f"{item['fragmento']}"
        )

        hash_id = hashlib.sha256(
            identificador.encode("utf-8")
        ).hexdigest()

        identificadores.append(hash_id)

    return identificadores


# ==========================================
# PROCESSAR UM DOCUMENTO
# ==========================================

def processar_documento(caminho):

    # Calcular hash do arquivo

    conteudo = caminho.read_bytes()

    hash_documento = hashlib.sha256(
        conteudo
    ).hexdigest()

    # Verificar se já está indexado

    if documento_ja_indexado(
        caminho.name,
        hash_documento
    ):

        return {
            "arquivo": caminho.name,
            "fragmentos": 0,
            "mensagem": "Documento já está atualizado.",
            "ignorado": True
        }

    # Extrair texto

    paginas = extrair_texto_pdf(caminho)

    # Dividir em fragmentos

    fragmentos = processar_paginas(paginas)

    if not fragmentos:

        remover_documento_indexado(
            caminho.name
        )

        return {
            "arquivo": caminho.name,
            "fragmentos": 0,
            "mensagem": "Nenhum texto extraível encontrado.",
            "ignorado": False
        }

    # Adicionar hash aos metadados

    for item in fragmentos:

        item["hash_documento"] = hash_documento

    # Preparar textos

    textos = [
        item["texto"]
        for item in fragmentos
    ]

    # Gerar embeddings

    embeddings = gerar_embeddings(textos)

    # Gerar identificadores

    identificadores = gerar_identificadores(
        fragmentos,
        hash_documento
    )

    # Remover versão anterior

    remover_documento_indexado(
        caminho.name
    )

    # Salvar nova versão

    quantidade = adicionar_fragmentos(
        fragmentos,
        embeddings,
        identificadores
    )

    return {
        "arquivo": caminho.name,
        "fragmentos": quantidade,
        "mensagem": "Documento indexado com sucesso.",
        "ignorado": False
    }


# ==========================================
# PROCESSAR VÁRIOS DOCUMENTOS
# ==========================================

def processar_varios_documentos(arquivos):

    resultados = []

    for arquivo in arquivos:

        try:

            resultado = processar_documento(
                arquivo
            )

            resultados.append({
                **resultado,
                "sucesso": True
            })

        except Exception as erro:

            resultados.append({
                "arquivo": arquivo.name,
                "fragmentos": 0,
                "mensagem": str(erro),
                "sucesso": False
            })

    return resultados
