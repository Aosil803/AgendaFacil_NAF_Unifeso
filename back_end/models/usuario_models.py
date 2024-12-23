from datetime import datetime
from sqlalchemy import CHAR, Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from back_end.create_db import Base
from back_end.models.login_models import Login

class Usuario(Base):
    __tablename__ = "usuario"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    perfil_usuario = Column(CHAR(25), nullable=False)
    email = Column(String, nullable=False)
    cpf = Column(String, unique=True, nullable=False)
    senha = Column(String, nullable=False)
    cep = Column(String, nullable=False)
    rua = Column(String, nullable=False)
    numero = Column(Integer, nullable=False)
    bairro = Column(String, nullable=False)
    complemento = Column(String, nullable=True)
    cidade = Column(String, nullable=False)
    estado = Column(String, nullable=False)
    telefone = Column(String, nullable=True)
    data_criacao = Column(Date, default=datetime.utcnow)
    id_login = Column(Integer, ForeignKey('login.id_login')) 
    login = relationship("Login") 
    agenda = relationship("Agenda", back_populates="usuario", uselist=False) 
