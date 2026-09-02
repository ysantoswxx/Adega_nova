document.addEventListener("DOMContentLoaded", function () {

    const botoes = document.querySelectorAll(".categorias button");
    const cards = document.querySelectorAll(".card-produto");
    const inputBusca = document.getElementById("input-busca");

    let categoriaSelecionada = "todos";


    botoes.forEach(function (botao) {

        botao.addEventListener("click", function () {

            // Remove o ativo dos outros botões
            botoes.forEach(function (btn) {
                btn.classList.remove("ativo");
            });

            // Ativa o botão clicado
            this.classList.add("ativo");

            // Pega a categoria do botão
            categoriaSelecionada = this.dataset.categoria
                .trim()
                .toLowerCase();

            filtrarProdutos();

        });

    });


    function filtrarProdutos() {

        const textoBusca = inputBusca
            ? inputBusca.value.trim().toLowerCase()
            : "";

        cards.forEach(function (card) {

            const categoriaProduto =
                (card.dataset.categoria || "")
                .trim()
                .toLowerCase();

            const nomeProduto =
                (card.dataset.nome || "")
                .trim()
                .toLowerCase();


            // Verifica a categoria
            const categoriaCorreta =
                categoriaSelecionada === "todos" ||
                categoriaProduto === categoriaSelecionada;


            // Verifica a pesquisa
            const nomeCorreto =
                nomeProduto.includes(textoBusca);


            // Mostra ou esconde
            if (categoriaCorreta && nomeCorreto) {
                card.style.display = "";
            } else {
                card.style.display = "none";
            }

        });

    }


    // Pesquisa pelo nome
    if (inputBusca) {
        inputBusca.addEventListener("input", function () {
            filtrarProdutos();
        });
    }

});