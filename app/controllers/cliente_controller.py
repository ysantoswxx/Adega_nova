# controllers/cliente_controller.py — CRUD de clientes
# ============================================================

from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.cliente import Cliente
from app.auth import get_admin

router = APIRouter(prefix="/clientes", tags=["Clientes"])
templates = Jinja2Templates(directory="app/templates")


# ============================================================
# LISTAR CLIENTES
# ============================================================

@router.get("/")
def listar_clientes(
    request: Request,
    busca: str = "",
    db: Session = Depends(get_db),
    admin=Depends(get_admin)
):
    query = db.query(Cliente)

    if busca:
        query = query.filter(
            Cliente.nome.ilike(f"%{busca}%") |
            Cliente.matricula.ilike(f"%{busca}%")
        )

    clientes = query.order_by(Cliente.nome).all()

    return templates.TemplateResponse(
        request,
        "clientes/index.html",
        {
            "request": request,
            "usuario": admin,
            "clientes": clientes,
            "busca": busca,
        }
    )


# ============================================================
# NOVO CLIENTE — FORMULÁRIO
# ============================================================

@router.get("/novo")
def form_novo(
    request: Request,
    admin=Depends(get_admin)
):
    return templates.TemplateResponse(
        request,
        "clientes/form.html",
        {
            "request": request,
            "usuario": admin,
            "editando": None
        }
    )


# ============================================================
# CRIAR CLIENTE
# ============================================================



# ============================================================
# EDITAR CLIENTE — FORMULÁRIO
# ============================================================

@router.get("/{cliente_id}/editar")
def form_editar(
    cliente_id: int,
    request: Request,
    db: Session = Depends(get_db),
    admin=Depends(get_admin)
):
    editando = db.query(Cliente).filter(
        Cliente.id == cliente_id
    ).first()

    if not editando:
        return RedirectResponse(
            url="/clientes",
            status_code=302
        )

    return templates.TemplateResponse(
        request,
        "clientes/form.html",
        {
            "request": request,
            "usuario": admin,
            "editando": editando
        }
    )


# ============================================================
# EDITAR CLIENTE
# ============================================================

@router.post("/{cliente_id}/editar")
def editar(
    cliente_id: int,
    nome: str = Form(...),
    matricula: str = Form(""),
    telefone: str = Form(""),
    db: Session = Depends(get_db),
    admin=Depends(get_admin)
):
    editando = db.query(Cliente).filter(
        Cliente.id == cliente_id
    ).first()

    if not editando:
        return RedirectResponse(
            url="/clientes",
            status_code=302
        )

    # Verifica conflito de matrícula
    if matricula:
        conflito = db.query(Cliente).filter(
            Cliente.matricula == matricula.strip(),
            Cliente.id != cliente_id
        ).first()

        if conflito:
            return RedirectResponse(
                url=f"/clientes/{cliente_id}/editar?erro=matricula",
                status_code=302
            )

    editando.nome = nome.strip()
    editando.matricula = matricula.strip() or None
    editando.telefone = telefone.strip() or None

    db.commit()

    return RedirectResponse(
        url="/clientes?editado=ok",
        status_code=302
    )


# ============================================================
# ATIVAR / DESATIVAR CLIENTE
# ============================================================

@router.post("/{cliente_id}/toggle-ativo")
def toggle_ativo(
    cliente_id: int,
    db: Session = Depends(get_db),
    admin=Depends(get_admin)
):
    cliente = db.query(Cliente).filter(
        Cliente.id == cliente_id
    ).first()

    if cliente:
        cliente.ativo = not cliente.ativo
        db.commit()

    return RedirectResponse(
        url="/clientes",
        status_code=302
    )