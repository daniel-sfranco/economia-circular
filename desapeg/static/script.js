var lastScrollTop = 0;

// function toggleSidebar() {
//     var sidebar = document.getElementById('sidebar');
//     var overlay = document.getElementById('overlay');
//     sidebar.classList.toggle('open');
//     overlay.classList.toggle('visible');
//     document.documentElement.classList.toggle('sidebar-open');
// }

window.addEventListener('scroll', function() {
    var st = window.pageYOffset || document.documentElement.scrollTop;
    var header = document.querySelector('header');
    if (st > lastScrollTop && st > 100) {
        // Se escrolar pra baixo, a header some
        header.classList.add('hidden');
    } else if (st < lastScrollTop) {
        // Se escrolar pra cima, ela volta
        header.classList.remove('hidden');
    }
    lastScrollTop = st <= 0 ? 0 : st;
});

document.addEventListener('click', function(event) {
    var sidebar = document.getElementById('sidebar');
    var overlay = document.getElementById('overlay');
    var hamburger = document.getElementById('hamburger');

    if (sidebar && sidebar.classList.contains('open') && !sidebar.contains(event.target) && !hamburger.contains(event.target)) {
        sidebar.classList.remove('open');
        overlay.classList.remove('visible');
        document.documentElement.classList.remove('sidebar-open');
    }
});

const overlayEl = document.getElementById('overlay');
if (overlayEl) {
    overlayEl.addEventListener('click', function() {
        document.getElementById('sidebar').classList.remove('open');
        this.classList.remove('visible');
        document.documentElement.classList.remove('sidebar-open');
    });
}

// Função de formatação de tempo (adicionada pelo seu amigo)
function formatElapsedTime(dataISO) {
    const now = new Date();
    const post = new Date(dataISO);
    const elapsedSeconds = Math.floor((now - post) / 1000);

    if (elapsedSeconds < 60) return "agora mesmo";

    const intervals = [
        { name: "ano", seconds: 31536000 },
        { name: "mês", seconds: 2592000 },
        { name: "dia", seconds: 86400 },
        { name: "hora", seconds: 3600 },
        { name: "minuto", seconds: 60 }
    ];

    for (const interval of intervals) {
        const count = Math.floor(elapsedSeconds / interval.seconds);
        if (count >= 1) {
            let unit = interval.name;
            if (count > 1) {
                unit = (unit === "mês") ? "meses" : unit + "s";
            }
            return `há ${count} ${unit}`;
        }
    }
}

// Função que cria o HTML do card
function createCard(produto) {
    const imagemFallback = '/static/assets/image_not_found.png';
    
    // Suporte tanto para os novos nomes da API (Name, Product_ID) quanto os antigos do JSON
    const nome = produto.name || produto.nome;
    const id = produto.product_id || produto.id || 1;
    const dataPostagem = produto.post_date || produto.tempo;
    
    // Se a data for ISO (tiver um 'T'), usa a formatação nova. Senão, mantém a original.
    const tempoFormatado = dataPostagem && dataPostagem.includes("T") ? formatElapsedTime(dataPostagem) : dataPostagem;

    return `
        <div class="item">
            <a href="product?id=${id}">
                <img 
                    src="${produto.imagem || imagemFallback}" 
                    alt="${nome}" 
                    onerror="this.onerror=null; this.src='${imagemFallback}';"
                >
                <div class="item-info">
                    <div class="item-title">${nome}</div>
                    <div class="item-time">${tempoFormatado}</div>
                </div>
            </a>
        </div>
    `;
}

// Função para buscar o JSON/API e montar um carrossel específico
function carregarCarrossel(endpoint, listId, sectionId, esconderSeVazio) {
    const section = document.getElementById(sectionId);
    const list = document.getElementById(listId);

    if (!section || !list) return;

    fetch(endpoint)
        .then(response => {
            if (!response.ok) throw new Error("Erro na rede");
            return response.json();
        })
        .then(data => {
            if (!data || data.length === 0) {
                if (esconderSeVazio) {
                    section.style.display = 'none';
                }
                return;
            }

            if (esconderSeVazio) {
                section.style.display = 'block';
            }
            
            list.innerHTML = data.map(produto => createCard(produto)).join('');
        })
        .catch(error => {
            console.error(`Erro ao carregar ${endpoint}:`, error);
            if (esconderSeVazio) {
                section.style.display = 'none';
            }
        });
}

// Inicializa os carrosséis usando a nova API para recomendados
carregarCarrossel('/api/products', 'recomendados-list', 'section-recomendados', false);
carregarCarrossel('vistos.json', 'vistos-list', 'section-vistos', true);

// Lógica das Setas para múltiplos carrosséis
document.querySelectorAll('.container').forEach(container => {
    const wrapper = container.querySelector('.gallery-wrapper');
    const btnLeft = container.querySelector('.arrow-left-control');
    const btnRight = container.querySelector('.arrow-right-control');

    if (wrapper && btnLeft && btnRight) {
        const scrollAmount = 300;

        btnLeft.addEventListener('click', () => {
            wrapper.scrollBy({
                top: 0,
                left: -scrollAmount,
                behavior: 'smooth'
            });
        });

        btnRight.addEventListener('click', () => {
            wrapper.scrollBy({
                top: 0,
                left: scrollAmount,
                behavior: 'smooth'
            });
        });
    }
});

window.addEventListener('scroll', function() {
    // Pega a quantidade de pixels que o usuário já rolou para baixo
    var scrollY = window.scrollY || window.pageYOffset;
    var hero = document.getElementById('hero');

    if (hero) {
        // Pega a altura total da janela do navegador do usuário
        var windowHeight = window.innerHeight;

        // Calcula a opacidade: começa em 1 (100% visível) no topo
        // e vai diminuindo até 0 conforme rola a página.
        var opacidade = 1 - (scrollY / (windowHeight * 0.9));

        opacidade = Math.max(0, Math.min(1, opacidade));
        hero.style.opacity = opacidade;
    }
});