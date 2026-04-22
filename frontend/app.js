// Camada de Apresentação - Lógica do Frontend
// Responsabilidade: capturar interações, chamar API, renderizar telas.
// Conhece apenas as URLs da API (não sabe como o backend está organizado).

const BASE_URL = "";

const telas = {
    home: document.getElementById("tela-home"),
    resultados: document.getElementById("tela-resultados"),
    detalhe: document.getElementById("tela-detalhe"),
    confirmacao: document.getElementById("tela-confirmacao"),
};

let livroAtual = null;


function mostrarTela(nome) {
    for (const chave in telas) {
        telas[chave].hidden = chave !== nome;
    }
    window.scrollTo({ top: 0, behavior: "smooth" });
}

function obterDataHojeISO() {
    const hoje = new Date();
    const ano = hoje.getFullYear();
    const mes = String(hoje.getMonth() + 1).padStart(2, "0");
    const dia = String(hoje.getDate()).padStart(2, "0");
    return `${ano}-${mes}-${dia}`;
}

async function buscarLivros(termo) {
    const url = `${BASE_URL}/api/livros?termo=${encodeURIComponent(termo)}`;
    const resposta = await fetch(url);
    const dados = await resposta.json();
    return { ok: resposta.ok, dados: dados };
}


async function buscarDetalheLivro(livroId) {
    const url = `${BASE_URL}/api/livros/${livroId}`;
    const resposta = await fetch(url);
    const dados = await resposta.json();
    return { ok: resposta.ok, dados: dados };
}


async function enviarReserva(livroId, unidade, usuario, data) {
    const url = `${BASE_URL}/api/reservas`;
    const corpo = {
        livro_id: livroId,
        unidade: unidade,
        usuario: usuario,
        data: data,
    };
    const resposta = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(corpo),
    });
    const dados = await resposta.json();
    return { ok: resposta.ok, dados: dados };
}


function renderizarResultados(termo, livros) {
    const texto = document.getElementById("texto-resultados");
    const grade = document.getElementById("grade-livros");

    if (livros.length === 0) {
        texto.textContent = `Nenhum livro encontrado para "${termo}".`;
        grade.innerHTML = "";
        return;
    }

    texto.textContent = `${livros.length} livro(s) encontrado(s) para "${termo}".`;
    grade.innerHTML = "";

    for (const livro of livros) {
        const numeroUnidades = livro.unidades_disponiveis.length;
        const totalTexto = livro.total_estoque === 1 ? "exemplar" : "exemplares";
        const unidadesTexto = numeroUnidades === 1 ? "unidade" : "unidades";

        const card = document.createElement("article");
        card.className = "book-card";
        card.innerHTML = `
            <div class="book-card__cover"></div>
            <div class="book-card__body">
                <span class="book-card__badge">${livro.badge}</span>
                <h3 class="book-card__title">${livro.titulo}</h3>
                <p class="book-card__meta">Autor: ${livro.autor}</p>
                <p class="book-card__meta">Editora: ${livro.editora}</p>
                <p class="book-card__meta">
                    ${livro.total_estoque} ${totalTexto} em ${numeroUnidades} ${unidadesTexto}
                </p>
                <div class="book-card__actions">
                    <button class="button button--primary" data-livro-id="${livro.id}">
                        Ver unidades
                    </button>
                </div>
            </div>
        `;
        grade.appendChild(card);
    }

    const botoes = grade.querySelectorAll("[data-livro-id]");
    for (const botao of botoes) {
        botao.addEventListener("click", function() {
            const id = parseInt(botao.getAttribute("data-livro-id"));
            abrirDetalhe(id);
        });
    }
}


function renderizarDetalhe(livro, unidades) {
    document.getElementById("detalhe-titulo").textContent = livro.titulo;
    document.getElementById("detalhe-meta").textContent = `${livro.autor} • ${livro.editora}`;
    document.getElementById("detalhe-badge").textContent = livro.badge;

    const lista = document.getElementById("lista-unidades");
    lista.innerHTML = "";

    if (unidades.length === 0) {
        lista.innerHTML = `<div class="results-message">Nenhuma unidade com estoque disponível para este livro.</div>`;
        return;
    }

    for (const unidade of unidades) {
        const quantidadeTexto = unidade.quantidade === 1
            ? "1 exemplar disponível"
            : `${unidade.quantidade} exemplares disponíveis`;

        const card = document.createElement("article");
        card.className = "unit-card";
        card.innerHTML = `
            <div>
                <h3 class="unit-card__title">${unidade.nome}</h3>
                <p class="unit-card__meta">${quantidadeTexto}</p>
            </div>
            <button class="button button--primary" data-unidade="${unidade.nome}">
                Reservar nesta unidade
            </button>
        `;
        lista.appendChild(card);
    }

    const botoes = lista.querySelectorAll("[data-unidade]");
    for (const botao of botoes) {
        botao.addEventListener("click", function() {
            const nomeUnidade = botao.getAttribute("data-unidade");
            realizarReserva(nomeUnidade);
        });
    }
}


function renderizarConfirmacao(reserva, livro, unidade) {
    const partes = [`${livro.titulo} reservado em ${unidade}.`];
    if (reserva.usuario) {
        partes.push(`Nome: ${reserva.usuario}`);
    }
    if (reserva.data) {
        partes.push(`Data: ${reserva.data}`);
    }

    document.getElementById("confirmacao-texto").textContent = partes.join(" • ");
    document.getElementById("confirmacao-qr-imagem").src = reserva.qr_code_imagem;
    document.getElementById("confirmacao-qr-codigo").textContent = reserva.qr_code;
}


async function executarBusca(termo) {
    const resultado = await buscarLivros(termo);

    if (!resultado.ok) {
        alert(resultado.dados.erro || "Erro ao buscar livros.");
        return;
    }

    renderizarResultados(resultado.dados.termo, resultado.dados.livros);
    mostrarTela("resultados");
}


async function abrirDetalhe(livroId) {
    const resultado = await buscarDetalheLivro(livroId);

    if (!resultado.ok) {
        alert(resultado.dados.erro || "Erro ao carregar livro.");
        return;
    }

    livroAtual = resultado.dados.livro;
    renderizarDetalhe(resultado.dados.livro, resultado.dados.unidades);

    const inputData = document.getElementById("input-data");
    inputData.min = obterDataHojeISO();

    mostrarTela("detalhe");
}


async function realizarReserva(unidade) {
    const usuario = document.getElementById("input-usuario").value.trim();
    const data = document.getElementById("input-data").value.trim();

    const resultado = await enviarReserva(livroAtual.id, unidade, usuario, data);

    if (!resultado.ok) {
        alert(resultado.dados.erro || "Erro ao realizar reserva.");
        return;
    }

    renderizarConfirmacao(resultado.dados.reserva, livroAtual, unidade);
    mostrarTela("confirmacao");
}


function voltarParaHome() {
    document.getElementById("input-busca").value = "";
    document.getElementById("input-usuario").value = "";
    document.getElementById("input-data").value = "";
    livroAtual = null;
    mostrarTela("home");
}


document.getElementById("form-busca").addEventListener("submit", function(evento) {
    evento.preventDefault();
    const termo = document.getElementById("input-busca").value.trim();
    if (termo === "") {
        alert("Digite um termo de busca.");
        return;
    }
    executarBusca(termo);
});


document.getElementById("link-home").addEventListener("click", function(evento) {
    evento.preventDefault();
    voltarParaHome();
});


document.getElementById("botao-nova-busca").addEventListener("click", function() {
    voltarParaHome();
});