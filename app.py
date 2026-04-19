import streamlit as st
import requests

# Configurações de Rede
API_URL = "http://192.168.0.200:8000/livros/"

st.set_page_config(page_title="Biblioteca SOA", layout="wide")
st.title("📚 Gestão de Biblioteca Online")

# Criando as abas para separar as funcionalidades
tab_lista, tab_cadastro, tab_editar = st.tabs(["📋 Acervo", "➕ Novo Livro", "⚙️ Gerenciar"])

# --- ABA 1: VISUALIZAÇÃO EM LISTA ---
with tab_lista:
    st.header("Livros Cadastrados")
    response = requests.get(API_URL)
    if response.status_code == 200:
        livros = response.json()
        if not livros:
            st.info("Nenhum livro cadastrado no momento.")
        else:
            st.table(livros)
    else:
        st.error("Erro ao conectar com o Web Service.")

# --- ABA 2: CADASTRO ---
with tab_cadastro:
    st.header("Cadastrar Livro")
    with st.form("form_cadastro"):
        col1, col2 = st.columns(2)
        with col1:
            titulo = st.text_input("Título")
            autor = st.text_input("Autor")
            ano = st.number_input("Ano", min_value=0, step=1)
        with col2:
            editora = st.text_input("Editora")
            localizacao = st.text_input("Localização")
            edicao = st.text_input("Edição")
        
        if st.form_submit_button("Salvar no Banco"):
            dados = {"titulo": titulo, "autor": autor, "ano": ano, 
                     "editora": editora, "localizacao": localizacao, "edicao": edicao}
            res = requests.post(API_URL, json=dados)
            if res.status_code == 200:
                st.success("Livro adicionado com sucesso!")
                st.rerun()

# --- ABA 3: EDIÇÃO E EXCLUSÃO ---
with tab_editar:
    st.header("Editar ou Remover Livros")
    response = requests.get(API_URL)
    if response.status_code == 200:
        livros = response.json()
        # Criar uma lista de títulos para o seletor
        opcoes = {f"{l['id']} - {l['titulo']}": l for l in livros}
        selecionado = st.selectbox("Selecione o livro para modificar:", options=opcoes.keys())
        
        if selecionado:
            livro_atual = opcoes[selecionado]
            
            # Campos preenchidos com os dados atuais para edição
            with st.container():
                st.subheader(f"Editando: {livro_atual['titulo']}")
                edit_titulo = st.text_input("Novo Título", value=livro_atual['titulo'])
                edit_autor = st.text_input("Novo Autor", value=livro_atual['autor'])
                
                col_del, col_upd = st.columns(2)
                
                # Botão de Exclusão (Método DELETE)
                if col_del.button("🗑️ Excluir Livro", type="primary"):
                    del_res = requests.delete(f"{API_URL}{livro_atual['id']}")
                    if del_res.status_code == 200:
                        st.warning("Livro removido!")
                        st.rerun()
                
                # Botão de Atualização (Método PUT)
                if col_upd.button("💾 Salvar Alterações"):
                    payload = {
                        "titulo": edit_titulo, "autor": edit_autor, 
                        "ano": livro_atual['ano'], "editora": livro_atual['editora'],
                        "localizacao": livro_atual['localizacao'], "edicao": livro_atual['edicao']
                    }
                    put_res = requests.put(f"{API_URL}{livro_atual['id']}", json=payload)
                    if put_res.status_code == 200:
                        st.success("Dados atualizados!")
                        st.rerun()