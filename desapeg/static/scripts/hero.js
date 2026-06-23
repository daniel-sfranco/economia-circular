window.addEventListener('scroll', function() {
    // Pega a quantidade de pixels que o usuário já rolou para baixo
    var scrollY = window.scrollY || window.pageYOffset;
    var hero = document.getElementById('hero');

    if (hero) {
        // Pega a altura total da janela do navegador do usuário
        var windowHeight = window.innerHeight;

        // Calcula a opacidade: começa em 1 (100% visível) no topo
        // e vai diminuindo até 0 conforme rola a página.
        var opacidade = 1 - (scrollY / (windowHeight * 0.9));

        opacidade = Math.max(0, Math.min(1, opacidade));
        hero.style.opacity = opacidade;
    }
});