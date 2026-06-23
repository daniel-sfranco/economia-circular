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

// Função que cria o HTML do card
function createCard(produto) {
    const imagemFallback = '/static/assets/image_not_found.png';
    
    // Suporte tanto para os novos nomes da API (Name, Product_ID) quanto os antigos do JSON
    const nome = produto.name || produto.nome;
    const id = produto.product_id || produto.id || 1;
    const dataPostagem = produto.post_date || produto.tempo;
    
    
    const tempoFormatado = dataPostagem && dataPostagem.includes("T") ? formatElapsedTime(dataPostagem) : dataPostagem;

    let imagemSrc = imagemFallback;

    if (produto.images && produto.images.length > 0) {
        imagemSrc = `/static/uploads/${produto.images[0]}`;
    } else if (produto.Image) {
        imagemSrc = produto.Image;
    }

    return `
        <div class="item">
            <a href="product?id=${id}">
                <img 
                    src="${imagemSrc}" 
                    alt="${nome}" 
                    onerror="this.onerror=null; this.src='${imagemFallback}';"
                >
                <div class="item-info">
                    <div class="item-title">${nome}</div>
                    <div class="item-time">${tempoFormatado}</div>
                </div>
            </a>
        </div>
    `;
}