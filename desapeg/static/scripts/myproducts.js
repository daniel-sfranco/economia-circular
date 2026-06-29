function confirmDelete(productId) {
        if(confirm("Tem certeza que deseja excluir este anúncio? Esta ação não poderá ser desfeita.")) {
            console.log(`Comando para deletar produto ID: ${productId}`);
            alert(`Simulação: O produto ${productId} foi excluído da interface.`);
        }
    }