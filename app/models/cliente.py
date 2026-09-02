from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from app.database import Base


class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    nome = Column(
        String(200),
        nullable=False
    )

    telefone = Column(
        String(20),
        nullable=True
    )

    cpf = Column(
        String(14),
        nullable=True
    )

    ativo = Column(
        Boolean,
        default=True,
        nullable=False
    )

    vendas = relationship(
        "Venda",
        back_populates="cliente"
    )

    def __repr__(self):
        return f"<Cliente {self.nome}>"