function simulateSave() {
    alert("Simulação: Alterações validadas e prontas para envio ao banco de dados!");
    window.location.href = "/myproducts";
}

function simulateDelete() {
    const confirmacao = confirm(
        "Você tem certeza absoluta? Essa operação vai deletar o produto e não poderá ser revertida."
    );
    
    if (confirmacao) {
        alert("Simulação: Produto apagado com sucesso.");
        window.location.href = "/myproducts";
    }
}