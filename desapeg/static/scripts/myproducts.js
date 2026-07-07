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