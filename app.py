import streamlit as st
import requests

# Configuração da API
BASE_URL = "http://192.168.0.200:8000"

API_URL = f"{BASE_URL}/livros/"
TOKEN_URL = f"{BASE_URL}/token"

st.set_page_config(
    page_title="Biblioteca",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Controle do token JWT
if "token" not in st.session_state:
    st.session_state.token = None

# Tela de login
if st.session_state.token is None:

    st.title("Login")

    usuario = st.text_input("Usuário")
    senha = st.text_input(
        "Senha",
        type="password"
    )

    if st.button("Entrar"):

        response = requests.post(
            TOKEN_URL,
            data={
                "username": usuario,
                "password": senha
            }
        )

        if response.status_code == 200:

            token = response.json()["access_token"]

            st.session_state.token = token

            st.success(
                "Login realizado com sucesso"
            )

            st.rerun()

        else:

            st.error(
                "Usuário ou senha inválidos"
            )

    st.stop()

# Cabeçalho
st.markdown("## Biblioteca")
st.markdown("---")

# Cabeçalho JWT
headers = {
    "Authorization": f"Bearer {st.session_state.token}"
}

# Controle de páginas
if "pagina" not in st.session_state:
    st.session_state.pagina = "Acervo"

def menu_item(nome):

    if st.sidebar.button(
        nome,
        use_container_width=True
    ):
        st.session_state.pagina = nome

with st.sidebar:

    st.markdown("### Menu")

    menu_item("Acervo")
    menu_item("Cadastro")
    menu_item("Gerenciar")

    st.markdown("---")

    if st.button("Sair"):

        st.session_state.token = None
        st.rerun()

menu = st.session_state.pagina

# Consulta de livros
def get_livros():

    try:

        response = requests.get(
            API_URL,
            headers=headers
        )

        return response.json()

    except:

        st.error(
            "Erro ao conectar com servidor"
        )

        return []

# Tela Acervo
if menu == "Acervo":

    st.subheader("Consulta")

    livros = get_livros()

    st.dataframe(
        livros,
        use_container_width=True
    )

# Tela Cadastro
elif menu == "Cadastro":

    st.subheader("Cadastro de livro")

    with st.form("form"):

        col1, col2 = st.columns(2)

        with col1:

            titulo = st.text_input("Título")
            autor = st.text_input("Autor")

            ano = st.number_input(
                "Ano",
                min_value=0
            )

        with col2:

            editora = st.text_input("Editora")
            localizacao = st.text_input("Localização")
            edicao = st.text_input("Edição")

        if st.form_submit_button("Salvar"):

            response = requests.post(
                API_URL,
                headers=headers,
                json={
                    "titulo": titulo,
                    "autor": autor,
                    "ano": ano,
                    "editora": editora,
                    "localizacao": localizacao,
                    "edicao": edicao
                }
            )

            if response.status_code == 200:

                st.success(
                    "Livro cadastrado"
                )

            else:

                st.error(
                    "Erro ao cadastrar"
                )

# Tela Gerenciar
elif menu == "Gerenciar":

    st.subheader("Atualização")

    livros = get_livros()

    if livros:

        op = {
            f"{l['id']} - {l['titulo']}": l
            for l in livros
        }

        sel = st.selectbox(
            "Selecionar",
            op.keys()
        )

        livro = op[sel]

        col1, col2 = st.columns(2)

        with col1:

            novo_titulo = st.text_input(
                "Título",
                value=livro["titulo"]
            )

            novo_autor = st.text_input(
                "Autor",
                value=livro["autor"]
            )

            novo_ano = st.number_input(
                "Ano",
                value=livro["ano"]
            )

        with col2:

            nova_editora = st.text_input(
                "Editora",
                value=livro["editora"]
            )

            nova_localizacao = st.text_input(
                "Localização",
                value=livro["localizacao"]
            )

            nova_edicao = st.text_input(
                "Edição",
                value=livro["edicao"]
            )

        col_btn1, col_btn2 = st.columns(2)

        if col_btn1.button("Excluir"):

            requests.delete(
                f"{API_URL}{livro['id']}",
                headers=headers
            )

            st.warning("Removido")
            st.rerun()

        if col_btn2.button("Atualizar"):

            requests.put(
                f"{API_URL}{livro['id']}",
                headers=headers,
                json={
                    "titulo": novo_titulo,
                    "autor": novo_autor,
                    "ano": novo_ano,
                    "editora": nova_editora,
                    "localizacao": nova_localizacao,
                    "edicao": nova_edicao
                }
            )

            st.success("Atualizado")
            st.rerun()