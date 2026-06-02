<h1>Sistema de Gestão de Biblioteca Online</h1>

Este projeto foi desenvolvido como parte da avaliação da disciplina de Arquitetura Orientada a Serviços. 
Trata-se de um ecossistema completo de gestão bibliotecária utilizando uma **Arquitetura Multicamadas**, integrando um Frontend interativo, um Web Service robusto e um banco de dados relacional persistente.

<br>
<h2>Arquitetura do Projeto</h2>
O sistema foi desenhado para rodar em um ambiente distribuído, simulando um cenário real de TI onde cada serviço reside em uma máquina (ou VM) diferente:

1.  **Camada de Apresentação (Frontend)**: Desenvolvida em **Streamlit (Python)**, rodando na máquina cliente. Ela consome os recursos do Web Service via requisições HTTP.
2.  **Camada de Negócio (Backend)**: Um Web Service construído com **FastAPI**, rodando em um servidor **Debian**. Ele gerencia as regras de negócio e a comunicação com o banco.
3.  **Camada de Dados (SGBD)**: Servidor **PostgreSQL** rodando em uma segunda instância **Debian**, responsável pela persistência e integridade das informações.7
<br>

<h2>Autenticação Baseada em JWT (JSON Web Token)</h2>
<p>A aplicação utiliza autenticação baseada em JWT para proteger os endpoints do Web Service.</p>

<h2>Fluxo de Autenticação</h2>
<p>O fluxo de autenticação funciona da seguinte forma:</p>
<ul>
    <li>
        <strong>Login do Usuário:</strong> Realizado através do endpoint:
        <code>POST /token</code>
    </li>
    <li>
        <strong>Geração de Token:</strong> A API valida as credenciais e gera um token JWT temporário.
    </li>
    <li>
        <strong>Envio do Token:</strong> O token é retornado ao cliente e deve ser enviado no cabeçalho das próximas requisições:
        <br><code>Authorization: Bearer TOKEN</code>
    </li>
    <li>
        <strong>Validação Automática:</strong> As rotas protegidas validam automaticamente:
        <ul>
            <li>Autenticidade do token</li>
            <li>Assinatura digital</li>
            <li>Tempo de expiração</li>
        </ul>
    </li>
    <li>
        <strong>Tratamento de Erro:</strong> Caso o token esteja inválido ou expirado, a API retorna:
        <br><code>401 Unauthorized</code>
    </li>
</ul>

<h2>Rotas Protegidas</h2>
<p>As seguintes rotas exigem autenticação JWT:</p>
<ul>
    <li><code>GET /livros/</code></li>
    <li><code>POST /livros/</code></li>
    <li><code>PUT /livros/{id}</code></li>
    <li><code>DELETE /livros/{id}</code></li>
</ul>

<h2>Configuração JWT</h2>
<ul>
    <li><strong>Algoritmo:</strong> HS256</li>
    <li><strong>Expiração do token:</strong> 30 minutos</li>
    <li><strong>Fluxo:</strong> OAuth2 Password Flow</li>
</ul>

<h2>Funcionamento da Segurança</h2>
<ul>
    <li>
        <strong>Validação no FastAPI:</strong> O sistema utiliza o mecanismo <code>Depends(get_current_user)</code> para validar automaticamente os tokens recebidos.
    </li>
    <li>
        <strong>Documentação Interativa:</strong> A documentação Swagger UI também integra autenticação JWT, permitindo realizar login diretamente pela interface <code>/docs</code>.
    </li>
</ul>

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
<br>
<h3>LivroBase</h3>
Utilizado para entrada de dados (POST e PUT). Recebe o que o usuário envia para o sistema.

```JSON
{
  "titulo": "string",
  "autor": "string",
  "ano": 0,
  "editora": "string",
  "localizacao": "string",
  "edicao": "string"
}
```


<h3>LivroResponse</h3>
Utilizado para saída de dados (Resposta da API). Inclui o id gerado pelo SGBD para permitir o rastreio do registro.

```JSON
{
  "id": 0,
  "titulo": "string",
  "autor": "string",
  "ano": 0,
  "editora": "string",
  "localizacao": "string",
  "edicao": "string"
}
```


<h3>Documentção API</h3>
<br>
<h3>HTTPValidationError (object)</h3>

```
    detail (array<object>)
        Items (object)
            loc (array<string | integer>)
                Items (string | integer)
                Any of (string | integer)
                    #0: string
                    #1: integer
    msg (string)
    type (string)
    input (any)
    ctx (object)
```

<h3>LivroBase (object)</h3>
Define a estrutura de dados para um livro na API. Recebe o que o usuário envia.

```
    titulo (string)
    autor (string)
    ano (integer)
    editora (string)
    localizacao (string)
    edicao (string)
```


<h3>LivroResponse (object)</h3>
Incrementa id para o modelo de resposta, permitindo que a API retorne o ID do livro criado ou listado.

```
    titulo (string)
    autor (string)
    ano (integer)
    editora (string)
    localizacao (string)
    edicao (string)
    id (integer)
```


<h3>ValidationError (object)</h3>

```
    loc (array<string | integer>)
        Items (string | integer)
        Any of (string | integer)
            #0: string
            #1: integer
    msg (string)
    type (string)
    input (any)
    ctx (object)
```



