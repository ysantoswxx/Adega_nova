javascript
// ==================================================
// CARRINHO
// ==================================================

let carrinho = [];


// ==================================================
// BOTÕES ADICIONAR
// ==================================================

document.querySelectorAll(".btn-adicionar").forEach(function(botao) {

    botao.addEventListener("click", function() {

        const card = this.closest(".card-produto");

        if (!card) {
            return;
        }

        const id = Number(card.dataset.id);
        const nome = card.dataset.nome;
        const preco = Number(card.dataset.preco);

        adicionarAoCarrinho(id, nome, preco);

    });

});


// ==================================================
// ADICIONAR PRODUTO
// ==================================================

function adicionarAoCarrinho(id, nome, preco) {

    preco = Number(preco);

    if (isNaN(preco)) {

        alert("Preço do produto inválido.");

        return;
    }

    const itemExistente = carrinho.find(
        item => item.id === id
    );

    if (itemExistente) {

        itemExistente.quantidade++;

    } else {

        carrinho.push({
            id: id,
            nome: nome,
            preco: preco,
            quantidade: 1
        });

    }

    atualizarCarrinho();
}


// ==================================================
// REMOVER PRODUTO
// ==================================================

function removerDoCarrinho(id) {

    carrinho = carrinho.filter(
        item => item.id !== id
    );

    atualizarCarrinho();
}


// ==================================================
// DIMINUIR QUANTIDADE
// ==================================================

function diminuirQuantidade(id) {

    const item = carrinho.find(
        item => item.id === id
    );

    if (!item) {
        return;
    }

    if (item.quantidade > 1) {

        item.quantidade--;

    } else {

        removerDoCarrinho(id);

        return;
    }

    atualizarCarrinho();
}


// ==================================================
// AUMENTAR QUANTIDADE
// ==================================================

function aumentarQuantidade(id) {

    const item = carrinho.find(
        item => item.id === id
    );

    if (!item) {
        return;
    }

    item.quantidade++;

    atualizarCarrinho();
}


// ==================================================
// ATUALIZAR CARRINHO
// ==================================================

function atualizarCarrinho() {

    const container =
        document.getElementById("itens-carrinho");

    const vazio =
        document.getElementById("vazio-carrinho");

    const rodape =
        document.getElementById("rodape-carrinho");

    const contador =
        document.getElementById("contador-itens");

    const totalEl =
        document.getElementById("valor-total");

    if (
        !container ||
        !vazio ||
        !rodape ||
        !contador ||
        !totalEl
    ) {
        return;
    }


    // ==================================================
    // QUANTIDADE TOTAL
    // ==================================================

    const totalItens = carrinho.reduce(
        (total, item) => {
            return total + item.quantidade;
        },
        0
    );


    // ==================================================
    // VALOR TOTAL
    // ==================================================

    const totalValor = carrinho.reduce(
        (total, item) => {
            return total + (
                item.preco * item.quantidade
            );
        },
        0
    );


    contador.textContent =
        `${totalItens} item(s)`;


    // ==================================================
    // CARRINHO VAZIO
    // ==================================================

    if (carrinho.length === 0) {

        vazio.style.display = "block";

        rodape.style.display = "none";

        container.innerHTML = "";

        totalEl.textContent = "R$ 0,00";

        return;
    }


    // ==================================================
    // CARRINHO COM PRODUTOS
    // ==================================================

    vazio.style.display = "none";

    rodape.style.display = "block";

    totalEl.textContent =
        formatarMoeda(totalValor);


    // ==================================================
    // MOSTRAR ITENS
    // ==================================================

    container.innerHTML = carrinho.map(function(item) {

        const subtotal =
            item.preco * item.quantidade;

        return `

            <div class="item-carrinho">

                <div class="item-info">

                    <h4>
                        ${escaparHTML(item.nome)}
                    </h4>

                    <span>
                        ${formatarMoeda(subtotal)}
                    </span>

                </div>

                <div class="item-quantidade">

                    <button
                        type="button"
                        onclick="diminuirQuantidade(${item.id})"
                    >
                        -
                    </button>

                    <span>
                        ${item.quantidade}
                    </span>

                    <button
                        type="button"
                        onclick="aumentarQuantidade(${item.id})"
                    >
                        +
                    </button>

                    <button
                        type="button"
                        onclick="removerDoCarrinho(${item.id})"
                    >
                        <i class="fa-solid fa-trash"></i>
                    </button>

                </div>

            </div>

        `;

    }).join("");
}


// ==================================================
// FORMATAR MOEDA
// ==================================================

function formatarMoeda(valor) {

    return "R$ " +
        Number(valor)
            .toFixed(2)
            .replace(".", ",");

}


// ==================================================
// ESCAPAR HTML
// ==================================================

function escaparHTML(texto) {

    const div =
        document.createElement("div");

    div.textContent = texto;

    return div.innerHTML;

}


// ==================================================
// FINALIZAR VENDA
// ==================================================

async function finalizarVenda() {

    if (carrinho.length === 0) {

        alert("O carrinho está vazio.");

        return;
    }

    const confirmar =
        confirm("Deseja finalizar esta venda?");

    if (!confirmar) {
        return;
    }

    try {

        const resposta = await fetch(
            "/vendas",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    itens: carrinho
                })
            }
        );


        if (!resposta.ok) {

            let mensagem =
                "Erro ao finalizar venda.";

            try {

                const erro =
                    await resposta.json();

                if (erro.detail) {
                    mensagem = erro.detail;
                }

            } catch (e) {

                console.error(
                    "Resposta não é JSON:",
                    e
                );

            }

            throw new Error(mensagem);
        }


        const dados =
            await resposta.json();

        console.log(
            "Venda realizada:",
            dados
        );


        alert(
            "Venda finalizada com sucesso!"
        );


        carrinho = [];

        atualizarCarrinho();

        location.reload();


    } catch (erro) {

        console.error(
            "Erro ao finalizar venda:",
            erro
        );

        alert(
            erro.message ||
            "Erro ao finalizar venda."
        );

    }

}


// ==================================================
// FILTRO DE CATEGORIA
// ==================================================

document
    .querySelectorAll(".categorias button")
    .forEach(function(botao) {

        botao.addEventListener(
            "click",
            function() {

                document
                    .querySelectorAll(
                        ".categorias button"
                    )
                    .forEach(function(b) {

                        b.classList.remove("ativo");

                    });


                this.classList.add("ativo");

                filtrarProdutos();

            }
        );

    });


// ==================================================
// FILTRAR PRODUTOS
// ==================================================

function filtrarProdutos() {

    const botaoAtivo =
        document.querySelector(
            ".categorias button.ativo"
        );

    const categoriaAtiva =
        botaoAtivo
            ? botaoAtivo.dataset.categoria
            : "todos";

    const campoBusca =
        document.getElementById(
            "input-busca"
        );

    const busca =
        campoBusca
            ? campoBusca.value
                .toLowerCase()
                .trim()
            : "";


    document
        .querySelectorAll(".card-produto")
        .forEach(function(card) {

            const cardCategoria =
                card.dataset.categoria || "";

            const cardNome =
                card.dataset.nome
                    ? card.dataset.nome.toLowerCase()
                    : "";

            const matchCategoria =
                categoriaAtiva === "todos" ||
                cardCategoria === categoriaAtiva;

            const matchBusca =
                cardNome.includes(busca);


            if (
                matchCategoria &&
                matchBusca
            ) {

                card.style.display = "";

            } else {

                card.style.display = "none";

            }

        });

}


// ==================================================
// PESQUISA
// ==================================================

const campoBusca =
    document.getElementById(
        "input-busca"
    );


if (campoBusca) {

    campoBusca.addEventListener(
        "input",
        filtrarProdutos
    );

}


// ==================================================
// INICIALIZAÇÃO
// ==================================================

atualizarCarrinho();

