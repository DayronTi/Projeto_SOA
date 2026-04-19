<h1>Sistema de Gestão de Biblioteca Online</h1>

Este projeto foi desenvolvido como parte da avaliação da disciplina de Arquitetura Orientada a Serviços. 
Trata-se de um ecossistema completo de gestão bibliotecária utilizando uma **Arquitetura Multicamadas**, integrando um Frontend interativo, um Web Service robusto e um banco de dados relacional persistente.

<br>
<h2>Arquitetura do Projeto</h2>
O sistema foi desenhado para rodar em um ambiente distribuído, simulando um cenário real de TI onde cada serviço reside em uma máquina (ou VM) diferente:

1.  **Camada de Apresentação (Frontend)**: Desenvolvida em **Streamlit (Python)**, rodando na máquina cliente. Ela consome os recursos do Web Service via requisições HTTP.
2.  **Camada de Negócio (Backend)**: Um Web Service construído com **FastAPI**, rodando em um servidor **Debian**. Ele gerencia as regras de negócio e a comunicação com o banco.
3.  **Camada de Dados (SGBD)**: Servidor **PostgreSQL** rodando em uma segunda instância **Debian**, responsável pela persistência e integridade das informações.

<br>
<h2>Configuração do Banco de Dados</h2>

Para o funcionamento correto, o SGBD deve conter uma base de dados chamada `biblioteca`.
### Estrutura da Tabela
A tabela `livros` deve ser criada com os seguintes campos obrigatórios conforme os requisitos do projeto:

```sql
CREATE DATABASE biblioteca;

\c biblioteca

CREATE TABLE livros (
    id SERIAL PRIMARY KEY,
    titulo VARCHAR(255) NOT NULL,
    autor VARCHAR(255) NOT NULL,
    ano INTEGER,
    editora VARCHAR(100),
    localizacao VARCHAR(100),
    edicao VARCHAR(50)
);
```

<br>
<h2>Endpoints do Web Service (API)</h2>

Entre no seu servidor backend e instale as dependencias
```
python -m pip install requirements.txt
```

Você também precisa de um arquivo .env contendo a URL do seu banco de dados

<br>
## Endpoints do Web Service (API)

A API foi documentada seguindo o padrão **REST**, utilizando o Swagger UI para testes. Os principais endpoints são:

| Método | Endpoint | Descrição |
| :--- | :--- | :--- |
| **GET** | `/livros/` | Lista todos os livros do acervo. |
| **POST** | `/livros/` | Cadastra um novo livro (autor, título, ano, editora, localização e edição). |
| **PUT** | `/livros/{id}` | Atualiza os dados de um livro existente através do seu ID. |
| **DELETE** | `/livros/{id}` | Remove permanentemente um livro do banco de dados. |

<br>
<h2>Como Executar</h2>

1. SGBD: Certifique-se de que o PostgreSQL está aceitando conexões remotas.

2. Backend
```python
uvicorn main:app --host 0.0.0.0 --port 8000
```

3. Frontend
```python
streamlit run app.py
```





