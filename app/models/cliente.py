from sqlalchemy import Column, Integer, String, Boolean
from app.database import Base
from sqlalchemy.orm import relationship


class Cliente(Base):
    __tablename__ = "clientes"

    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(200), nullable=False)
    telefone = Column(String(20), nullable=True)
    email = Column(String(200), nullable=True)
    cpf = Column(String(14), nullable=True)
    ativo = Column(Boolean, default=True)

    # Relacionamento reverso para consultar vendas do cliente
    vendas = relationship("Venda", back_populates="cliente")

    def __repr__(self):
        return f"<Cliente {self.nome}>"
