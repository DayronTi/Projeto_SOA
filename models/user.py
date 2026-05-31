from pydantic import BaseModel

class User(BaseModel):
    """
    Modelo responsável por representar os dados de autenticação
    utilizados durante o processo de login da API.
    """

    username: str
    password: str