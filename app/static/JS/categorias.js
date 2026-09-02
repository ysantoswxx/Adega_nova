document.addEventListener("DOMContentLoaded", function () {

    const botoes = document.querySelectorAll(".categorias button");
    const produtos = document.querySelectorAll(".card-produto");
    const busca = document.getElementById("input-busca");

    let categoriaSelecionada = "todos";


    function filtrarProdutos() {

        const textoBusca = busca.value
            .toLowerCase()
            .trim();


        produtos.forEach(function (produto) {

            const categoria = (
                produto.dataset.categoria || ""
            ).toLowerCase().trim();


            const nome = (
                produto.dataset.nome || ""
            ).toLowerCase().trim();


            const categoriaFiltro =
                categoriaSelecionada.toLowerCase().trim();


            const correspondeCategoria =
                categoriaFiltro === "todos" ||
                categoria === categoriaFiltro;


            const correspondeBusca =
                nome.includes(textoBusca);


            if (correspondeCategoria && correspondeBusca) {

                produto.style.display = "";

            } else {

                produto.style.display = "none";

            }

        });
    }


    botoes.forEach(function (botao) {

        botao.addEventListener("click", function () {

            botoes.forEach(function (b) {
                b.classList.remove("ativo");
            });


            this.classList.add("ativo");


            categoriaSelecionada =
                this.dataset.categoria;


            filtrarProdutos();

        });

    });


    busca.addEventListener("input", function () {

        filtrarProdutos();

    });


    filtrarProdutos();

});