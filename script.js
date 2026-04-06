var lastScrollTop = 0;

function toggleSidebar() {
    var sidebar = document.getElementById('sidebar');
    var overlay = document.getElementById('overlay');
    sidebar.classList.toggle('open');
    overlay.classList.toggle('visible');
    document.documentElement.classList.toggle('sidebar-open');
}

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

// ==========================================
// 2. Lógica da Página Inicial (Carrossel)
// ==========================================

// Função que cria o HTML do card
function createCard(produto) {
    const imagemFallback = 'assets/image_not_found.png';
    return `
        <div class="item">
            <img 
                src="${produto.imagem || imagemFallback}" 
                alt="${produto.nome}" 
                onerror="this.onerror=null; this.src='${imagemFallback}';"
            >
            <div class="item-info">
                <div class="item-title">${produto.nome}</div>
                <div class="item-time">${produto.tempo}</div>
            </div>
        </div>
    `;
}

// Função para buscar o JSON e montar um carrossel específico
function carregarCarrossel(jsonFile, listId, sectionId, esconderSeVazio) {
    const section = document.getElementById(sectionId);
    const list = document.getElementById(listId);

    // Se não existir o elemento HTML na página (ex: página Sobre), interrompe
    if (!section || !list) return;

    fetch(jsonFile)
        .then(response => response.json())
        .then(data => {
            // Se o JSON estiver vazio ou não tiver dados
            if (!data || data.length === 0) {
                if (esconderSeVazio) {
                    section.style.display = 'none'; // Esconde tudo
                }
                return; // O CSS (.gallery:empty) vai segurar o espaço do "Recomendados"
            }

            // Se tem dados, garante que a seção esteja visível e insere os cards
            if (esconderSeVazio) {
                section.style.display = 'block';
            }
            
            // Junta todos os cards e joga dentro da lista
            list.innerHTML = data.map(produto => createCard(produto)).join('');
        })
        .catch(error => {
            console.error(`Erro ao carregar ${jsonFile}:`, error);
            // Se der erro (ex: arquivo não existe) e for pra esconder, esconde
            if (esconderSeVazio) {
                section.style.display = 'none';
            }
        });
}

// Inicializa os dois carrosséis (Arquivo JSON, ID da Lista, ID da Seção, Esconder se vazio?)
carregarCarrossel('recomendados.json', 'recomendados-list', 'section-recomendados', false);
carregarCarrossel('vistos.json', 'vistos-list', 'section-vistos', true);


// Lógica das Setas para múltiplos carrosséis
// Encontra todos os containers de carrossel na página
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