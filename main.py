import os
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from typing import List
from dotenv import load_dotenv

from auth.jwt_handler import (
    create_access_token,
    verify_token
)

load_dotenv()

# Configuração do banco de dados
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

# Modelo da tabela livros
class LivroDB(Base):
    """
    Define a estrutura da tabela livros no banco de dados.
    """

    __tablename__ = "livros"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String)
    autor = Column(String)
    ano = Column(Integer)
    editora = Column(String)
    localizacao = Column(String)
    edicao = Column(String)

Base.metadata.create_all(bind=engine)

# Modelo utilizado para entrada de dados
class LivroBase(BaseModel):
    titulo: str
    autor: str
    ano: int
    editora: str
    localizacao: str
    edicao: str

# Modelo utilizado nas respostas da API
class LivroResponse(LivroBase):
    id: int

    class Config:
        from_attributes = True

app = FastAPI(
    title="Web Service Biblioteca Online"
)

# Usuário de teste para autenticação
fake_user = {
    "username": "admin",
    "password": "123456"
}

# Configuração do JWT
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token"
)

# Sessão do banco de dados
def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()

# Endpoint responsável pelo login
@app.post("/token")
def login(
    form_data: OAuth2PasswordRequestForm = Depends()
):

    if (
        form_data.username != fake_user["username"]
        or
        form_data.password != fake_user["password"]
    ):
        raise HTTPException(
            status_code=401,
            detail="Usuário ou senha inválidos"
        )

    access_token = create_access_token(
        data={
            "sub": form_data.username
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

# Validação do token recebido
def get_current_user(
    token: str = Depends(oauth2_scheme)
):

    payload = verify_token(token)

    if payload is None:
        raise HTTPException(
            status_code=401,
            detail="Token inválido ou expirado"
        )

    return payload

# Página inicial da API
@app.get("/")
def home():

    return {
        "mensagem": "Web Service de Integração de Biblioteca Ativo"
    }

# Cadastro de livros
@app.post(
    "/livros/",
    response_model=LivroResponse
)
def criar_livro(
    livro: LivroBase,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    db_livro = LivroDB(**livro.dict())

    db.add(db_livro)
    db.commit()
    db.refresh(db_livro)

    return db_livro

# Consulta de livros
@app.get(
    "/livros/",
    response_model=List[LivroResponse]
)
def listar_livros(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    return db.query(LivroDB).all()

# Atualização de livros
@app.put(
    "/livros/{livro_id}",
    response_model=LivroResponse
)
def atualizar_livro(
    livro_id: int,
    livro_atualizado: LivroBase,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    db_livro = (
        db.query(LivroDB)
        .filter(LivroDB.id == livro_id)
        .first()
    )

    if not db_livro:
        raise HTTPException(
            status_code=404,
            detail="Livro não encontrado"
        )

    for key, value in livro_atualizado.dict().items():
        setattr(db_livro, key, value)

    db.commit()
    db.refresh(db_livro)

    return db_livro

# Exclusão de livros
@app.delete("/livros/{livro_id}")
def deletar_livro(
    livro_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    db_livro = (
        db.query(LivroDB)
        .filter(LivroDB.id == livro_id)
        .first()
    )

    if not db_livro:
        raise HTTPException(
            status_code=404,
            detail="Livro não encontrado"
        )

    db.delete(db_livro)
    db.commit()

    return {
        "mensagem": f"Livro {livro_id} deletado com sucesso"
    }