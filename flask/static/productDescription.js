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
            // Alterna a classe 'active' no botão (para girar a setinha)
            this.classList.toggle("active");
            
            // Alterna a classe 'show' na descrição (para abrir/fechar a caixa)
            descriptionDiv.classList.toggle("show");
        });
    }
});