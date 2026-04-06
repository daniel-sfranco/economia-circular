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

const container = document.getElementById('product-list');

if (container) {
    fetch('/api/products') 
        .then(response => {
            if (!response.ok) throw new Error("Erro na rede");
            return response.json();
        })
        .then(data => {
            data.forEach(produto => {
                const card = document.createElement('div');
                card.classList.add('item');
                
                const imagemFallback = '/static/assets/image_not_found.png';
                card.innerHTML = `
                <a href="product?id=${produto.Product_ID}">
                    <img 
                        src="${produto.imagem || imagemFallback}" 
                        alt="${produto.Name}" 
                        onerror="this.onerror=null; this.src='${imagemFallback}';"
                    >
                    <div class="item-info">
                        <div class="item-title">${produto.Name}</div>
                        <div class="item-time">${formatElapsedTime(produto.Post_Date)}</div>
                    </div>\
                </a>
                `;

                container.appendChild(card);
            });
        })
        .catch(error => console.error("Erro ao carregar o JSON:", error));
}

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