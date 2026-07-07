const productId = document
    .querySelector(".product-registration-container")
    .dataset.productId;

async function saveProduct() {

    const name = document.getElementById("product-name").value;
    const description = document.getElementById("product-description").value;
    const condition = document.getElementById("product-condition").value;
    const cost = document.getElementById("product-cost").value;
    const quantity = document.getElementById("product-quantity").value;
    const usageTime = document.getElementById("product-usage-time").value;
    const pickupLocation = document.getElementById("product-pickup-location").value;
    const categories = document.getElementById("hidden-categories").value;
    const imageFiles = document.getElementById("image-upload").files;

    const formData = new FormData();

    formData.append("name", name);
    formData.append("description", description);
    formData.append("condition", condition);
    formData.append("cost", cost);
    formData.append("quantity", quantity);
    formData.append("usage_time", usageTime);
    formData.append("pickup_location", pickupLocation);
    formData.append("categories", categories);
    for (const image of imageFiles) {
        formData.append("images", image);
    }

    const response = await fetch(
        `/api/product/${productId}`,
        {
            method: "PUT",
            body: formData
        }
    );

    const data = await response.json();

    //console.log(data);
    if (response.ok) {
        alert("Produto atualizado com sucesso!");
        window.location.href = "/myproducts";
    }
}

const categoryInput = document.getElementById('category-input');
const hiddenCategories = document.getElementById('hidden-categories');
const tagsContainer = document.getElementById('tags-container');
const dropdownList = document.getElementById('autocomplete-list');

if (categoryInput) {
    let availableCategories = [];
    let selectedTags = hiddenCategories.value
    ? hiddenCategories.value.split(',').map(t => t.trim())
    : [];

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

    selectedTags.forEach(tag => createTag(tag));

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

async function deleteProduct(productId) {
    const confirmacao = confirm(
        "Você tem certeza absoluta? Essa operação vai deletar o produto e não poderá ser revertida."
    );

    if (!confirmacao) {
        return;
    }

    const response = await fetch(
        `/api/product/${productId}`,
        {
            method: "DELETE"
        }
    );

    const data = await response.json();

    if (response.ok) {
        alert("Produto excluído com sucesso!");
        window.location.href = "/myproducts";
    }
}