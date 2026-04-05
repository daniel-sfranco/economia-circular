// ==========================================
// 1. Lógica Geral (Menu, Scroll e Overlay)
// ==========================================
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

// Verifica se o container de produtos existe na página atual antes de rodar o fetch
const container = document.getElementById('product-list');

if (container) {
    fetch('produtos.json')
        .then(response => response.json())
        .then(data => {
            data.forEach(produto => {
                const card = document.createElement('div');
                card.classList.add('item');

                card.innerHTML = `
                    <img src="${produto.imagem}" alt="${produto.nome}">
                    <div class="item-info">
                        <div class="item-title">${produto.nome}</div>
                        <div class="item-time">${produto.tempo}</div>
                    </div>
                `;

                container.appendChild(card);
            });
        })
        .catch(error => console.error("Erro ao carregar o JSON:", error));
}

// Verifica se os controles do carrossel existem na página atual
const galleryScroll = document.getElementById('gallery-scroll');
const btnLeft = document.querySelector('.arrow-left-control');
const btnRight = document.querySelector('.arrow-right-control');

if (galleryScroll && btnLeft && btnRight) {
    const scrollAmount = 300;

    btnLeft.addEventListener('click', () => {
        galleryScroll.scrollBy({
            top: 0,
            left: -scrollAmount,
            behavior: 'smooth'
        });
    });

    btnRight.addEventListener('click', () => {
        galleryScroll.scrollBy({
            top: 0,
            left: scrollAmount,
            behavior: 'smooth'
        });
    });
}