window.onload = function () {
    const params = (new URL(document.location)).searchParams;
    const produtId = params.get('id');
    loadInfo(produtId)
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

function loadInfo(id) {
  fetch(`/api/productInfo/${id}`)
    .then(response => {
      if (!response.ok) {
        throw new Error('Erro ao buscar produto');
      }
      return response.json();
    })
    .then(data => {
      // 1. Preenche os Textos
      document.getElementById("prodName").innerHTML = data.product_name;
      document.getElementById("seller").innerHTML = data.seller;
      document.getElementById("description").innerHTML = data.description;
      document.getElementById("date").innerHTML = formatElapsedTime(data.post_date);

      let priceNum = parseFloat(data.cost);
      if (priceNum === 0 || isNaN(priceNum)){
        document.getElementById("cost").innerHTML = "DOAÇÃO";
      } else {
        document.getElementById("cost").innerHTML = "R$ " + priceNum.toFixed(2).replace('.',',');
      }
      document.getElementById("quantity").innerHTML = "Quantidade: " + data.quantity;

      const mainImageEl = document.getElementById("product-main-image"); 
      const thumbnailsContainer = document.getElementById("product-thumbnails");
      const fallbackImage = '/static/assets/image_not_found.png';

      let imagesArray = data.images;

      // Fallback: Se não houver imagens, usa a padrão e esconde as miniaturas
      if (!imagesArray || !Array.isArray(imagesArray) || imagesArray.length === 0) {
          console.log("Nenhuma imagem no JSON. Imagem de fallback ativada.");
          if (mainImageEl) mainImageEl.src = fallbackImage;
          if (thumbnailsContainer) thumbnailsContainer.style.display = 'none';
      } else {
          // Limita a 5 imagens
          imagesArray = imagesArray.slice(0, 5);

          // Define a primeira imagem como a principal inicial
          if (mainImageEl) mainImageEl.src = imagesArray[0];
          
          if (thumbnailsContainer) {
              thumbnailsContainer.style.display = 'flex';
              thumbnailsContainer.innerHTML = ''; // Limpa caso haja algo antes

              // Cria as miniaturas dinamicamente
              imagesArray.forEach((imgUrl, index) => {
                  const thumb = document.createElement('img');
                  thumb.src = imgUrl;
                  thumb.className = 'thumbnail-img';
                  
                  // Se for a primeira miniatura, já começa com a borda de "ativa"
                  if (index === 0) {
                      thumb.classList.add('active');
                  }

                  // Evento de clique para trocar a imagem principal
                  thumb.addEventListener('click', function() {
                      // Troca o src da imagem grande
                      mainImageEl.src = imgUrl;

                      // Remove a classe 'active' de todas as miniaturas
                      document.querySelectorAll('.thumbnail-img').forEach(t => t.classList.remove('active'));
                      // Adiciona a classe 'active' apenas na miniatura clicada
                      this.classList.add('active');
                  });

                  thumbnailsContainer.appendChild(thumb);
              });
          }
      }
    })
    .catch(error => {
      console.error("Erro na requisição:", error);
    });
}


document.addEventListener("DOMContentLoaded", function() {
    const toggleBtn = document.getElementById("descToggle");
    const descriptionDiv = document.getElementById("description");

    if (toggleBtn && descriptionDiv) {
        toggleBtn.addEventListener("click", function() {
            this.classList.toggle("active");
            descriptionDiv.classList.toggle("show");
        });
    }

    const modal = document.getElementById("imageModal");
    const fullImage = document.getElementById("fullImage");
    const mainImageEl = document.getElementById("product-main-image");

    if (mainImageEl && modal && fullImage) {
        
        // Abre o modal ao clicar na imagem do produto
        mainImageEl.addEventListener("click", function() {
            modal.style.display = "flex"; 
            fullImage.src = this.src;     
        });

        // Fecha o modal se o usuário clicar no fundo preto
        modal.addEventListener("click", function(event) {
            if (event.target === modal) {
                modal.style.display = "none";
            }
        });
    }
});