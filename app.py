import streamlit as st
import requests

# ===== CONFIG =====
API_URL = "http://192.168.0.200:8000/livros/"
MODO_OFFLINE = False

st.set_page_config(
    page_title="Biblioteca",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ===== HEADER =====
st.markdown("## Biblioteca")
st.markdown("---")

# ===== MENU =====
if "pagina" not in st.session_state:
    st.session_state.pagina = "Acervo"

def menu_item(nome):
    if st.sidebar.button(nome, use_container_width=True):
        st.session_state.pagina = nome

with st.sidebar:
    st.markdown("### Menu")

    menu_item("Acervo")
    menu_item("Cadastro")
    menu_item("Gerenciar")

    st.markdown("---")

menu = st.session_state.pagina

# ===== DADOS =====
def get_livros():
    try:
        return requests.get(API_URL).json()
    except:
        st.error("Erro ao conectar com servidor")
        return []

# ===== ACERVO =====
if  menu == "Acervo":
    st.subheader("Consulta")

    livros = get_livros()

    st.dataframe(livros, use_container_width=True)

# ===== CADASTRO =====
elif menu == "Cadastro":
    st.subheader("Cadastro de livro")

    with st.form("form"):
        col1, col2 = st.columns(2)

        with col1:
            titulo = st.text_input("Título")
            autor = st.text_input("Autor")
            ano = st.number_input("Ano", min_value=0)

        with col2:
            editora = st.text_input("Editora")
            localizacao = st.text_input("Localização")
            edicao = st.text_input("Edição")

        if st.form_submit_button("Salvar"):
            if MODO_OFFLINE:
                st.success("Registro salvo")
            else:
                requests.post(API_URL, json={
                    "titulo": titulo,
                    "autor": autor,
                    "ano": ano,
                    "editora": editora,
                    "localizacao": localizacao,
                    "edicao": edicao
                })
                st.success("Cadastrado")

# ===== GERENCIAR =====
elif menu == "Gerenciar":
    st.subheader("Atualização")

    livros = get_livros()

    if livros:
        op = {f"{l['id']} - {l['titulo']}": l for l in livros}
        sel = st.selectbox("Selecionar", op.keys())

        livro = op[sel]

        col1, col2 = st.columns(2)

        with col1:
            novo_titulo = st.text_input("Título", value=livro["titulo"])
            novo_autor = st.text_input("Autor", value=livro["autor"])
            novo_ano = st.number_input("Ano", value=livro["ano"])

        with col2:
            nova_editora = st.text_input("Editora", value=livro["editora"])
            nova_localizacao = st.text_input("Localização", value=livro["localizacao"])
            nova_edicao = st.text_input("Edição", value=livro["edicao"])

        col_btn1, col_btn2 = st.columns(2)

        if col_btn1.button("Excluir"):
            if MODO_OFFLINE:
                st.warning("Exclusão simulada")
            else:
                requests.delete(f"{API_URL}{livro['id']}")
                st.warning("Removido")
                st.rerun()

        if col_btn2.button("Atualizar"):
            if MODO_OFFLINE:
                st.success("Atualização simulada")
            else:
                requests.put(f"{API_URL}{livro['id']}", json={
                    "titulo": novo_titulo,
                    "autor": novo_autor,
                    "ano": novo_ano,
                    "editora": nova_editora,
                    "localizacao": nova_localizacao,
                    "edicao": nova_edicao
                })
                st.success("Atualizado")
                st.rerun()