import os
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from typing import List, Optional
from dotenv import load_dotenv

load_dotenv()

# --- CONFIGURAÇÃO DO BANCO DE DADOS ---
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- MODELO DE PERSISTÊNCIA (SGBD) ---
class LivroDB(Base):
    """
    Define como a tabela 'livros' será estruturada no banco de dados, com colunas para id, título, autor, ano, editora, localização e edição.
    """
    __tablename__ = "livros"
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String)
    autor = Column(String)
    ano = Column(Integer)
    editora = Column(String)
    localizacao = Column(String)
    edicao = Column(String)

# Cria a tabela se ela não existir
Base.metadata.create_all(bind=engine)

# --- MODELO DE VALIDAÇÃO (API) ---
class LivroBase(BaseModel):
    """
    Define a estrutura de dados para um livro na API. Recebe o que o usuário envia
    """
    titulo: str
    autor: str
    ano: int
    editora: str
    localizacao: str
    edicao: str

class LivroResponse(LivroBase):
    """
    Incrementa id para o modelo de resposta, permitindo que a API retorne o ID do livro criado ou listado.
    """
    id: int

    class Config:
        from_attributes = True

# --- INICIALIZAÇÃO ---
app = FastAPI(title="Web Service Biblioteca Online")

# Dependência para o banco de dados
def get_db():
    """
    Garante que cada requisição tenha uma sessão de banco de dados independente, 
    que é aberta no início da requisição e fechada ao final, evitando conexões persistentes ou vazamentos de conexões.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --- ROTAS / ENDPOINTS ---
@app.get("/") # @ é usado para decorar a função home, associando-a à rota raiz ("/") do aplicativo FastAPI. Isso significa que quando um cliente fizer uma requisição GET para a URL base do aplicativo, a função home será executada e sua resposta será retornada ao cliente.
def home():
    return {"mensagem": "Web Service de Integração de Biblioteca Ativo"}

# 1. FUNÇÃO DE CRIAR LIVROS (POST)
@app.post("/livros/", response_model=LivroResponse)
def criar_livro(livro: LivroBase, db: Session = Depends(get_db)):
    """
    Recebe um JSON, tranforma em um objeto LivroDB e adiciona ao banco usando commit.
    """
    db_livro = LivroDB(**livro.dict())
    db.add(db_livro)
    db.commit()
    db.refresh(db_livro)
    return db_livro

# 2. FUNÇÃO DE LISTAR LIVROS (GET)
@app.get("/livros/", response_model=List[LivroResponse])
def listar_livros(db: Session = Depends(get_db)):
    return db.query(LivroDB).all()

# 3. FUNÇÃO DE ATUALIZAR LIVROS (PUT)
@app.put("/livros/{livro_id}", response_model=LivroResponse)
def atualizar_livro(livro_id: int, livro_atualizado: LivroBase, db: Session = Depends(get_db)):
    """
    Busca pelo ID no banco de dados, percorre os campos enviados e atualiza o registro correspondente.
    """
    db_livro = db.query(LivroDB).filter(LivroDB.id == livro_id).first()
    if not db_livro:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    
    for key, value in livro_atualizado.dict().items():
        setattr(db_livro, key, value)
    
    db.commit()
    db.refresh(db_livro)
    return db_livro

# 4. FUNÇÃO DE DELETAR LIVROS (DELETE)
@app.delete("/livros/{livro_id}")
def deletar_livro(livro_id: int, db: Session = Depends(get_db)):
    """
    Deleta um livro do banco de dados com base no ID fornecido.
    """
    db_livro = db.query(LivroDB).filter(LivroDB.id == livro_id).first() # Verifica se o livro existe no banco de dados
    if not db_livro:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    
    db.delete(db_livro)
    db.commit()
    return {"mensagem": f"Livro {livro_id} deletado com sucesso"}