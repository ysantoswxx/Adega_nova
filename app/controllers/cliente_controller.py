# controllers/cliente_controller.py — CRUD de clientes
# ============================================================

from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.cliente import Cliente
from app.auth import get_admin


router = APIRouter(
    prefix="/clientes",
    tags=["Clientes"]
)

templates = Jinja2Templates(
    directory="app/templates"
)


# ============================================================
# LISTAR CLIENTES
# ============================================================

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

    # Pesquisa por nome ou telefone
    if busca:
        query = query.filter(
            Cliente.nome.ilike(f"%{busca}%") |
            Cliente.telefone.ilike(f"%{busca}%")
        )

<<<<<<< Updated upstream
    clientes = query.order_by(
        Cliente.nome
    ).all()
=======
    clientes = query.order_by(Cliente.nome).all()
>>>>>>> Stashed changes

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
<<<<<<< Updated upstream
# FORMULÁRIO — NOVO CLIENTE
=======
# NOVO CLIENTE — FORMULÁRIO
>>>>>>> Stashed changes
# ============================================================

@router.get("/novo")
def form_novo(
    request: Request,
    admin=Depends(get_admin)
):
<<<<<<< Updated upstream

=======
>>>>>>> Stashed changes
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

@router.post("/novo")
def criar(
    request: Request,
<<<<<<< Updated upstream

    nome: str = Form(...),

    telefone: str = Form(""),

    db: Session = Depends(get_db),

    admin=Depends(get_admin)
):

    # --------------------------------------------------------
<<<<<<< HEAD
=======
    # VERIFICA SE A MATRÍCULA JÁ EXISTE
    # --------------------------------------------------------

=======
    nome: str = Form(...),
    matricula: str = Form(""),
    telefone: str = Form(""),
    db: Session = Depends(get_db),
    admin=Depends(get_admin)
):
    # Verifica duplicidade de matrícula
>>>>>>> Stashed changes
    if matricula:

        existente = db.query(Cliente).filter(
            Cliente.matricula == matricula.strip()
        ).first()

        if existente:

            return templates.TemplateResponse(
                request,
                "clientes/form.html",
                {
                    "request": request,
                    "usuario": admin,
                    "editando": None,
<<<<<<< Updated upstream

                    "erro":
                        f"Matrícula {matricula} já cadastrada.",

=======
                    "erro": f"Matrícula {matricula} já cadastrada.",
>>>>>>> Stashed changes
                    "valores": {
                        "nome": nome,
                        "matricula": matricula,
                        "telefone": telefone
                    }
                },

                status_code=400
            )

<<<<<<< Updated upstream

    # --------------------------------------------------------
>>>>>>> 05b9e0835263100d1eacd9736d1b46f673498221
    # CRIA CLIENTE
    # --------------------------------------------------------

    cliente = Cliente(
        nome=nome.strip(),

        telefone=(
            telefone.strip()
            if telefone
            else None
        )
    )

    db.add(cliente)

    db.commit()

<<<<<<< HEAD
=======
=======
    cliente = Cliente(
        nome=nome.strip(),
        matricula=matricula.strip() or None,
        telefone=telefone.strip() or None,
    )

    db.add(cliente)
    db.commit()

    return RedirectResponse(
        url="/clientes?criado=ok",
        status_code=302
    )
>>>>>>> Stashed changes

>>>>>>> 05b9e0835263100d1eacd9736d1b46f673498221
    return RedirectResponse(
        url="/clientes?criado=ok",
        status_code=302
    )


# ============================================================
# FORMULÁRIO — EDITAR CLIENTE
# ============================================================

# ============================================================
# EDITAR CLIENTE — FORMULÁRIO
# ============================================================

@router.get("/{cliente_id}/editar")
def form_editar(
    cliente_id: int,

    request: Request,

    db: Session = Depends(get_db),
<<<<<<< Updated upstream

    admin=Depends(get_admin)
):

=======
    admin=Depends(get_admin)
):
>>>>>>> Stashed changes
    editando = db.query(Cliente).filter(
        Cliente.id == cliente_id
    ).first()

<<<<<<< HEAD
=======
<<<<<<< Updated upstream

>>>>>>> 05b9e0835263100d1eacd9736d1b46f673498221
    # Cliente não encontrado
    if not editando:

=======
    if not editando:
>>>>>>> Stashed changes
        return RedirectResponse(
            url="/clientes",
            status_code=302
        )
<<<<<<< Updated upstream

<<<<<<< HEAD
=======
=======
>>>>>>> Stashed changes

>>>>>>> 05b9e0835263100d1eacd9736d1b46f673498221
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
<<<<<<< Updated upstream

    nome: str = Form(...),

    telefone: str = Form(""),

    db: Session = Depends(get_db),

    admin=Depends(get_admin)
):

    editando = db.query(Cliente).filter(
        Cliente.id == cliente_id
    ).first()

    # Cliente não encontrado
    if not editando:

        return RedirectResponse(
            url="/clientes",
            status_code=302
        )

<<<<<<< HEAD
=======

    # --------------------------------------------------------
    # VERIFICA CONFLITO DE MATRÍCULA
    # --------------------------------------------------------
=======
    nome: str = Form(...),
    matricula: str = Form(""),
    telefone: str = Form(""),
    db: Session = Depends(get_db),
    admin=Depends(get_admin)
):
    editando = db.query(Cliente).filter(
        Cliente.id == cliente_id
    ).first()
>>>>>>> Stashed changes

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

<<<<<<< Updated upstream

=======
>>>>>>> Stashed changes
        if conflito:

            return RedirectResponse(

                url=
                f"/clientes/{cliente_id}/editar?erro=matricula",

                status_code=302

            )

<<<<<<< Updated upstream

>>>>>>> 05b9e0835263100d1eacd9736d1b46f673498221
    # --------------------------------------------------------
    # ATUALIZA CLIENTE
    # --------------------------------------------------------

    editando.nome = nome.strip()

    editando.telefone = (
        telefone.strip()
        if telefone
        else None
    )

    db.commit()

<<<<<<< HEAD
=======
=======
    editando.nome = nome.strip()
    editando.matricula = matricula.strip() or None
    editando.telefone = telefone.strip() or None

    db.commit()

    return RedirectResponse(
        url="/clientes?editado=ok",
        status_code=302
    )
>>>>>>> Stashed changes

>>>>>>> 05b9e0835263100d1eacd9736d1b46f673498221
    return RedirectResponse(
        url="/clientes?editado=ok",
        status_code=302
    )


# ============================================================
# ATIVAR / DESATIVAR CLIENTE
# ============================================================

# ============================================================
# ATIVAR / DESATIVAR CLIENTE
# ============================================================

@router.post("/{cliente_id}/toggle-ativo")
def toggle_ativo(
    cliente_id: int,

    db: Session = Depends(get_db),
<<<<<<< Updated upstream

    admin=Depends(get_admin)
):

=======
    admin=Depends(get_admin)
):
>>>>>>> Stashed changes
    cliente = db.query(Cliente).filter(
        Cliente.id == cliente_id
    ).first()

<<<<<<< HEAD
=======
<<<<<<< Updated upstream

=======
>>>>>>> Stashed changes
>>>>>>> 05b9e0835263100d1eacd9736d1b46f673498221
    if cliente:

        cliente.ativo = not cliente.ativo

        db.commit()

<<<<<<< HEAD
=======
<<<<<<< Updated upstream

=======
>>>>>>> Stashed changes
>>>>>>> 05b9e0835263100d1eacd9736d1b46f673498221
    return RedirectResponse(
        url="/clientes",
        status_code=302
    )