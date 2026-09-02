from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.usuarios import Usuario
from app.auth import hash_senha, verificar_senha, criar_token

router = APIRouter(prefix="/auth", tags=["Autenticação"])
templates = Jinja2Templates(directory="app/templates")


@router.get("/login", response_class=HTMLResponse)
def tela_login(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="auth/login.html",
        context={"erro": None},
    )


@router.post("/login", response_class=HTMLResponse)
def fazer_login(
    request: Request,
    senha: str = Form(...),
    # Aceita o campo correto "email" e também o campo antigo "usuario".
    email: str | None = Form(None),
    usuario: str | None = Form(None),
    db: Session = Depends(get_db),
):
    email_digitado = (email or usuario or "").strip().lower()

    if not email_digitado:
        return templates.TemplateResponse(
            request=request,
            name="auth/login.html",
            context={"erro": "Digite o e-mail cadastrado."},
            status_code=400,
        )

    usuario_db = (
        db.query(Usuario)
        .filter(Usuario.email.ilike(email_digitado))
        .first()
    )

    if usuario_db is None:
        return templates.TemplateResponse(
            request=request,
            name="auth/login.html",
            context={"erro": "E-mail ou senha incorretos."},
            status_code=401,
        )

    if not usuario_db.senha_hash or not verificar_senha(senha, usuario_db.senha_hash):
        return templates.TemplateResponse(
            request=request,
            name="auth/login.html",
            context={"erro": "E-mail ou senha incorretos."},
            status_code=401,
        )

    if usuario_db.ativo is False:
        return templates.TemplateResponse(
            request=request,
            name="auth/login.html",
            context={"erro": "Usuário inativo. Contate o administrador."},
            status_code=403,
        )

    token_data = {
        "sub": usuario_db.email,
        "nome": usuario_db.nome,
        "role": usuario_db.role,
        "id": usuario_db.id,
    }
    token = criar_token(token_data)

    response = RedirectResponse(url="/", status_code=303)
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        max_age=3600,
        samesite="lax",
        secure=False,  # Use True somente quando estiver em HTTPS.
    )
    return response


@router.get("/logout")
def sair(request: Request):
    response = RedirectResponse(url="/auth/login", status_code=303)
    response.delete_cookie(key="access_token")
    return response
