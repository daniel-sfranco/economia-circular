document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('.product-form');
    if (form) {
        form.reset();
    }

    const fileInput = document.getElementById('image-upload');
    const previewContainer = document.getElementById('image-preview-container');
    const modal = document.getElementById('image-modal');
    const modalImg = document.getElementById('modal-image');

    if (fileInput) {
        fileInput.addEventListener('change', function() {
            previewContainer.innerHTML = '';
            
            // Transforma os arquivos selecionados em uma lista
            const files = Array.from(this.files);
            const filesToProcess = files.slice(0, 5);

            filesToProcess.forEach(file => {
                // Confirma se é realmente uma imagem
                if (file.type.startsWith('image/')) {
                    const reader = new FileReader();
                    
                    reader.onload = function(e) {
                        // Cria a tag <img> dinamicamente
                        const img = document.createElement('img');
                        img.src = e.target.result;
                        img.classList.add('preview-thumbnail');
                        
                        img.addEventListener('click', function() {
                            modalImg.src = this.src;
                            modal.style.display = 'flex'; 
                        });
                        
                        previewContainer.appendChild(img);
                    }
                    
                    // Lê o arquivo do computador do usuário
                    reader.readAsDataURL(file);
                }
            });
        });
    }

    if (modal) {
        modal.addEventListener('click', function(e) {
            if (e.target === modal) {
                modal.style.display = 'none';
            }
        });
    }
});

const categoryInput = document.getElementById('category-input');
const hiddenCategories = document.getElementById('hidden-categories');
const tagsContainer = document.getElementById('tags-container');
const dropdownList = document.getElementById('autocomplete-list');

if (categoryInput) {
    let availableCategories = [];
    let selectedTags = [];

    fetch('/api/categorias')
        .then(res => res.json())
        .then(data => { availableCategories = data; })
        .catch(err => console.error("Erro ao carregar categorias:", err));

    function updateHiddenInput() {
        hiddenCategories.value = selectedTags.join(',');
    }

    function createTag(text) {
        const tag = document.createElement('div');
        tag.className = 'tag';
        tag.innerHTML = `
            ${text}
            <span class="remove-tag" data-val="${text}">&times;</span>
        `;
            
        tag.querySelector('.remove-tag').addEventListener('click', function() {
            const val = this.getAttribute('data-val');
            selectedTags = selectedTags.filter(t => t !== val);
            tag.remove();
            updateHiddenInput();
        });
        
        tagsContainer.insertBefore(tag, categoryInput);
    }

    categoryInput.addEventListener('input', function() {
        const val = this.value.toLowerCase();
        dropdownList.innerHTML = '';
        
        if (!val) {
            dropdownList.style.display = 'none';
            return;
        }
        const filtered = availableCategories.filter(cat => 
            cat.toLowerCase().includes(val) && !selectedTags.includes(cat)
        );
        
        if (filtered.length > 0) {
            filtered.forEach(cat => {
                const item = document.createElement('div');
                item.textContent = cat;
                item.addEventListener('click', function() {
                    selectedTags.push(cat);
                    createTag(cat);
                    categoryInput.value = ''; // limpa o input
                    dropdownList.style.display = 'none';
                    updateHiddenInput();
                });
                dropdownList.appendChild(item);
            });
            dropdownList.style.display = 'block';
        } else {
            dropdownList.style.display = 'none';
        }
    });

    categoryInput.addEventListener('keydown', function(e) {
        if (e.key === 'Enter') {
            e.preventDefault();
        }
    });

    document.addEventListener('click', function(e) {
        if (e.target !== categoryInput && e.target !== dropdownList) {
            dropdownList.style.display = 'none';
        }
    });
}