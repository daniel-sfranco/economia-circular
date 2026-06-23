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