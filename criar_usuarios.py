# Script para criar ou atualizar o usuário administrador

from app.database import SessionLocal
from app.models.usuarios import Usuario
from app.auth import hash_senha


def seed():
    db = SessionLocal()

    try:
        nome_usuario = "admin"
        email_usuario = "admin@teste.com"
        senha_usuario = "admin@123"
        perfil = "admin"

        existente = (
            db.query(Usuario)
            .filter_by(email=email_usuario)
            .first()
        )

        if existente is None:
            usuario = Usuario(
                nome=nome_usuario,
                email=email_usuario,
                senha_hash=hash_senha(senha_usuario),
                role=perfil,
                ativo=True,
            )
            db.add(usuario)
            print("Usuário admin criado com sucesso!")
        else:
            existente.nome = nome_usuario
            existente.senha_hash = hash_senha(senha_usuario)
            existente.role = perfil
            existente.ativo = True
            print("Usuário admin atualizado com sucesso!")

        db.commit()

    except Exception as erro:
        db.rollback()
        print(f"Erro ao criar ou atualizar o usuário admin: {erro}")

    finally:
        db.close()


if __name__ == "__main__":
    seed()
