var lastScrollTop = 0;

function toggleUserSidebar() {
    var sidebar = document.getElementById('user-sidebar');
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
    var sidebar = document.getElementById('user-sidebar');
    var overlay = document.getElementById('overlay');
    var user_btn = document.getElementById('user-btn');

    if (sidebar && sidebar.classList.contains('open') && !sidebar.contains(event.target) && !user_btn.contains(event.target)) {
        sidebar.classList.remove('open');
        overlay.classList.remove('visible');
        document.documentElement.classList.remove('sidebar-open');
    }
});

const overlayEl = document.getElementById('overlay');
if (overlayEl) {
    overlayEl.addEventListener('click', function() {
        document.getElementById('user-sidebar').classList.remove('open');
        this.classList.remove('visible');
        document.documentElement.classList.remove('sidebar-open');
    });
}

// Funções relacionadas com a pesquisa de produtos
const searchForm = document.getElementById('search-form');
const searchInput = document.getElementById('search-input');
const searchBtn = document.getElementById('search-btn');

if (searchForm && searchInput && searchBtn) {
    searchBtn.addEventListener('click', function(e) {
        if (!searchForm.classList.contains('active')) {
            e.preventDefault();
            searchForm.classList.add('active');
            searchInput.focus();
        } else {
            if (searchInput.value.trim() === '') {
                e.preventDefault();
                searchForm.classList.remove('active');
            }
        }
    });

    document.addEventListener('click', function(e) {
        if (!searchForm.contains(e.target) && searchForm.classList.contains('active')) {
            if (searchInput.value.trim() === '') {
                searchForm.classList.remove('active');
            }
        }
    });
}

const searchDropdown = document.getElementById('search-dropdown');
let searchTimeout;

if (searchInput && searchDropdown) {
    searchInput.addEventListener('input', function() {
        clearTimeout(searchTimeout);
        const query = this.value.trim();

        if (query.length === 0) {
            searchDropdown.classList.remove('active');
            return;
        }

        searchTimeout = setTimeout(() => {
            fetch(`/api/search?q=${encodeURIComponent(query)}`)
                .then(response => response.json())
                .then(data => {
                    searchDropdown.innerHTML = '';

                    if (data.length === 0) {
                        searchDropdown.innerHTML = '<div class="search-dropdown-empty">Nenhum produto encontrado.</div>';
                    } else {
                        data.forEach(produto => {
                            const imagemFallback = '/static/assets/image_not_found.png';
                            let imagemSrc = imagemFallback;

                            if (produto.images && produto.images.length > 0) {
                                imagemSrc = `/static/uploads/${produto.images[0]}`;
                            } else if (produto.image_paths) {
                                imagemSrc = `/static/uploads/${produto.image_paths.split(',')[0]}`;
                            } else if (produto.Image) {
                                imagemSrc = produto.Image;
                            }

                            const valorPreco = parseFloat(produto.cost);
                            let precoExibicao;

                            if (isNaN(valorPreco) || valorPreco === 0) {
                                precoExibicao = "DOAÇÃO";
                            } else {
                                precoExibicao = `R$ ${valorPreco.toFixed(2).replace('.', ',')}`;
                            }

                            const item = document.createElement('a');
                            item.href = `/product?id=${produto.id}`;
                            item.className = 'search-dropdown-item';

                            item.innerHTML = `
                                <img src="${imagemSrc}" alt="${produto.name}" class="search-dropdown-img" onerror="this.onerror=null; this.src='${imagemFallback}';">
                                <div class="search-dropdown-info">
                                    <span class="search-dropdown-title">${produto.name}</span>
                                    <span class="search-dropdown-price">${precoExibicao}</span>
                                </div>
                            `;
                            searchDropdown.appendChild(item);

                        });
                    }
                    searchDropdown.classList.add('active');
                })
                .catch(err => console.error("Erro na busca ao vivo:", err));
        }, 300);
    });

    document.addEventListener('click', function(e) {
        if (!searchForm.contains(e.target) && !searchDropdown.contains(e.target)) {
            searchDropdown.classList.remove('active');
        }
    });
}