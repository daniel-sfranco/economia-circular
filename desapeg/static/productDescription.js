window.onload = function () {
    const params = (new URL(document.location)).searchParams;
    const produtId = params.get('id');
    loadInfo(produtId)
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
      document.getElementById("prodName").innerHTML = data.name;
      document.getElementById("seller").innerHTML = data.seller;
      document.getElementById("cost").innerHTML = data.cost;
      document.getElementById("date").innerHTML = data.post_date;
      document.getElementById("quantity").innerHTML = data.quantity;
      document.getElementById("description").innerHTML = data.description;
    })
    .catch(error => {
      console.error("Erro na requisição:", error);
    });
}