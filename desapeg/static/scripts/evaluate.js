document.addEventListener('DOMContentLoaded', () => {
    const stars = document.querySelectorAll('.star');
    const ratingInput = document.getElementById('rating');
    const ratingHelp = document.getElementById('rating-help');

    const labels = {
        1: 'Péssima',
        2: 'Ruim',
        3: 'Boa',
        4: 'Muito boa',
        5: 'Excelente'
    };

    const setRating = (value) => {
        ratingInput.value = value;
        stars.forEach((star, index) => {
            const starValue = index + 1;
            star.classList.toggle('active', starValue <= value);
        });

        ratingHelp.textContent = value ? `Sua avaliação: ${labels[value]}` : 'Selecione uma nota';
    };

    stars.forEach((star) => {
        star.addEventListener('click', () => {
            const value = Number(star.dataset.value);
            setRating(value);
        });

        star.addEventListener('mouseenter', () => {
            const value = Number(star.dataset.value);
            stars.forEach((item, index) => {
                item.classList.toggle('hovered', index < value);
            });
        });

        star.addEventListener('mouseleave', () => {
            stars.forEach((item) => item.classList.remove('hovered'));
        });
    });
});
