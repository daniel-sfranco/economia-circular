document.addEventListener('DOMContentLoaded', () => {

    const categoriasSelecionadasElement =
        document.getElementById('categorias-selecionadas');

    const categoriasSelecionadas =
        categoriasSelecionadasElement
            ? JSON.parse(
                categoriasSelecionadasElement.dataset.categorias
              )
            : [];

    const precoRange = document.getElementById('preco-max');
    const precoDisplay = document.getElementById('preco-display');

    if (precoRange && precoDisplay) {
        precoRange.addEventListener('input', (e) => {
            const valor = parseFloat(e.target.value).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });
            precoDisplay.textContent = `Até ${valor}`;
        });
    }

    fetch('/api/categorias')
        .then(response => response.json())
        .then(data => {
            const container = document.getElementById('categorias-container');
            
            data.forEach(categoria => {
                const label = document.createElement('label');
                label.className = 'checkbox-item';

                const checked = categoriasSelecionadas.includes(categoria)
                    ? 'checked'
                    : '';

                label.innerHTML = `
                    <input
                        type="checkbox"
                        name="categoria"
                        value="${categoria}"
                        ${checked}
                    >
                    ${categoria}
                `;

                container.appendChild(label);
            });
        })
        .catch(err => {
            console.error("Erro ao carregar as categorias:", err);
            document.getElementById('categorias-container').innerHTML = '<span style="color:red; font-size:0.85rem;">Erro ao carregar categorias.</span>';
        });
});

const rangeMin = document.getElementById('preco-min');
const rangeMax = document.getElementById('preco-max');
const track = document.getElementById('slider-track');
const displayMin = document.getElementById('preco-min-display');
const displayMax = document.getElementById('preco-max-display');

if (rangeMin && rangeMax) {
    const maxLimit = parseInt(rangeMax.max);
    const minGap = 50;
    function updateSlider(e) {
        let minVal = parseInt(rangeMin.value);
        let maxVal = parseInt(rangeMax.value);
        if (maxVal - minVal < minGap) {
            if (e.target.id === 'preco-min') {
                rangeMin.value = maxVal - minGap;
                minVal = parseInt(rangeMin.value);
            } else {
                rangeMax.value = minVal + minGap;
                maxVal = parseInt(rangeMax.value);
            }
        }
        const percentMin = (minVal / maxLimit) * 100;
        const percentMax = (maxVal / maxLimit) * 100;
        
        track.style.left = percentMin + "%";
        track.style.width = (percentMax - percentMin) + "%";
        displayMin.textContent = `R$ ${minVal.toLocaleString('pt-BR')}`;
        
        if (maxVal >= maxLimit) {
            displayMax.textContent = `R$ ${maxLimit.toLocaleString('pt-BR')} e mais`;
        } else {
            displayMax.textContent = `R$ ${maxVal.toLocaleString('pt-BR')}`;
        }
    }
    rangeMin.addEventListener('input', updateSlider);
    rangeMax.addEventListener('input', updateSlider);
    
    updateSlider({target: rangeMax});
}