from modules.chatbot import responder

from modules.document_indexer import (
    processar_varios_documentos
)

from modules.vector_database import (
    contar_fragmentos,
    listar_documentos_indexados
)


import streamlit as st

from config.config import (
    inicializar_sistema,
    MODELO_CHAT,
    MODELO_EMBEDDING
)

from modules.document_manager import (
    adicionar_documento,
    listar_documentos,
    excluir_documento,
    contar_documentos,
    informacoes_documentos
)


# ==========================================
# CONFIGURAÇÕES DA PÁGINA
# ==========================================

st.set_page_config(
    page_title="Chatbot de Documentos",
    page_icon="📚",
    layout="wide"
)


# ==========================================
# INICIALIZAÇÃO
# ==========================================

inicializar_sistema()


# ==========================================
# CABEÇALHO
# ==========================================

st.title("📚 Assistente de Documentos")

st.caption(
    "Gerencie seus documentos PDF e consulte informações utilizando inteligência artificial local."
)


# ==========================================
# BARRA LATERAL
# ==========================================

with st.sidebar:

    st.header("⚙️ Configurações")

    st.write("**Modelo de conversa:**")
    st.code(MODELO_CHAT)

    st.write("**Modelo de embeddings:**")
    st.code(MODELO_EMBEDDING)

    st.divider()

    st.metric(
        "Documentos cadastrados",
        contar_documentos()
    )


# ==========================================
# UPLOAD DE DOCUMENTOS
# ==========================================

st.subheader("📄 Gerenciamento de documentos")

arquivos = st.file_uploader(
    "Selecione seus arquivos PDF",
    type=["pdf"],
    accept_multiple_files=True
)


if st.button(
    "Adicionar documentos",
    use_container_width=True,
    disabled=not arquivos
):

    sucessos = 0

    erros = []

    with st.spinner("Adicionando documentos..."):

        for arquivo in arquivos:

            try:

                resultado = adicionar_documento(arquivo)

                if resultado["duplicado"]:

                    st.info(
                        resultado["mensagem"]
                    )

                else:

                    sucessos += 1

            except Exception as erro:

                erros.append(
                    f"{arquivo.name}: {erro}"
                )

    if sucessos:

        st.success(
            f"{sucessos} documento(s) adicionado(s)!"
        )

    for erro in erros:

        st.error(erro)

    st.rerun()


# ==========================================
# LISTAGEM DOS DOCUMENTOS
# ==========================================

st.divider()

st.subheader("📚 Documentos disponíveis")

documentos = informacoes_documentos()

if documentos:

    st.write(
        f"Total de documentos: **{len(documentos)}**"
    )

    for documento in documentos:

        with st.container(border=True):

            col1, col2, col3 = st.columns(
                [5, 2, 2]
            )

            with col1:

                st.write(
                    f"📄 **{documento['nome']}**"
                )

            with col2:

                tamanho = documento["tamanho"] / 1024

                st.caption(
                    f"{tamanho:.2f} KB"
                )

            with col3:

                if st.button(
                    "🗑️ Excluir",
                    key=f"excluir_{documento['nome']}",
                    use_container_width=True
                ):

                    try:

                        excluir_documento(
                            documento["nome"]
                        )

                        st.success(
                            "Documento excluído!"
                        )

                        st.rerun()

                    except Exception as erro:

                        st.error(str(erro))

else:

    st.info(
        "Nenhum documento cadastrado. "
        "Adicione um PDF para começar."
    )


# ==========================================
# PROCESSAMENTO DOS DOCUMENTOS
# ==========================================

st.divider()

st.subheader("⚙️ Indexação dos documentos")

documentos = listar_documentos()

if documentos:

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Fragmentos indexados",
            contar_fragmentos()
        )

    with col2:

        st.metric(
            "PDFs indexados",
            len(listar_documentos_indexados())
        )

    if st.button(
        "📄 Processar documentos",
        use_container_width=True
    ):

        with st.spinner(
            "Extraindo textos e gerando embeddings..."
        ):

            resultados = processar_varios_documentos(
                documentos
            )

        for resultado in resultados:

            if resultado["sucesso"]:

                st.success(
                    f"{resultado['arquivo']}: "
                    f"{resultado['fragmentos']} fragmentos. "
                    f"{resultado['mensagem']}"
                )

            else:

                st.error(
                    f"{resultado['arquivo']}: "
                    f"{resultado['mensagem']}"
                )

        st.rerun()

else:

    st.info(
        "Adicione documentos PDF para iniciar a indexação."
    )


# ==========================================
# ÁREA DE PESQUISA INTELIGENTE
# ==========================================

st.divider()

st.subheader("🔎 Faça uma pergunta sobre seus documentos")

quantidade_fragmentos = contar_fragmentos()

if quantidade_fragmentos == 0:

    st.info(
        "Ainda não existem documentos indexados. "
        "Adicione e processe um PDF para começar."
    )

else:

    st.caption(
        f"Base de conhecimento disponível: "
        f"{quantidade_fragmentos} fragmentos indexados."
    )

    with st.form("formulario_pergunta"):

        pergunta = st.text_area(
            "Digite sua pergunta:",
            placeholder="Ex.: Quais são os principais assuntos abordados neste documento?",
            height=100
        )

        enviar = st.form_submit_button(
            "🔎 Consultar documentos",
            use_container_width=True
        )

    if enviar:

        if not pergunta.strip():

            st.warning(
                "Digite uma pergunta antes de continuar."
            )

        else:

            try:

                with st.spinner(
                    "Analisando documentos e gerando resposta..."
                ):

                    resposta, fontes = responder(
                        pergunta
                    )

                st.subheader("💬 Resposta")

                st.markdown(resposta)

                if fontes:

                    with st.expander(
                        "📚 Fontes consultadas",
                        expanded=True
                    ):

                        for fonte in fontes:

                            st.write(f"📄 {fonte}")

                else:

                    st.caption(
                        "Nenhuma fonte foi identificada."
                    )

            except Exception as erro:

                st.error(
                    f"Não foi possível responder: {erro}"
                )
