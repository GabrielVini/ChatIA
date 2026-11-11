
import pymupdf

from pathlib import Path

from config.config import (
    EXTENSOES_PERMITIDAS,
    TAMANHO_MINIMO_TEXTO
)


# ==========================================
# VALIDAR DOCUMENTO
# ==========================================

def validar_pdf(caminho):

    caminho = Path(caminho)

    if not caminho.exists():
        raise FileNotFoundError(
            f"Arquivo não encontrado: {caminho.name}"
        )

    if caminho.suffix.lower() not in EXTENSOES_PERMITIDAS:
        raise ValueError(
            "Formato não permitido. Envie um arquivo PDF."
        )

    if caminho.stat().st_size == 0:
        raise ValueError("O arquivo PDF está vazio.")

    return True


# ==========================================
# EXTRAIR TEXTO DO PDF
# ==========================================

def extrair_texto_pdf(caminho):

    caminho = Path(caminho)

    validar_pdf(caminho)

    paginas = []

    try:

        documento = pymupdf.open(caminho)

        try:

            if documento.is_encrypted:
                raise ValueError(
                    f"O PDF {caminho.name} está protegido por senha."
                )

            for numero, pagina in enumerate(
                documento,
                start=1
            ):

                texto = pagina.get_text("text")

                texto = texto.strip()

                if len(texto) < TAMANHO_MINIMO_TEXTO:
                    continue

                paginas.append({
                    "arquivo": caminho.name,
                    "pagina": numero,
                    "texto": texto
                })

        finally:
            documento.close()

    except ValueError:
        raise

    except Exception as erro:

        raise RuntimeError(
            f"Erro ao ler o PDF {caminho.name}: {erro}"
        ) from erro

    return paginas


# ==========================================
# PROCESSAR VÁRIOS PDFs
# ==========================================

def extrair_texto_varios_pdfs(arquivos):

    resultados = []

    for arquivo in arquivos:

        paginas = extrair_texto_pdf(arquivo)

        resultados.extend(paginas)

    return resultados
