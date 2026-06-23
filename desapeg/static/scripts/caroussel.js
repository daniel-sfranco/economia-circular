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