document.addEventListener("DOMContentLoaded", function () {
    const faqHeaders = document.querySelectorAll(".faq-header");

    faqHeaders.forEach(header => {
        header.addEventListener("click", function () {
            const content = this.nextElementSibling;

            // Alternar la clase "active" para el ícono
            this.classList.toggle("active");

            // Alternar la altura máxima del contenido
            if (content.style.maxHeight) {
                content.style.maxHeight = null; // Cierra el contenido
            } else {
                content.style.maxHeight = content.scrollHeight + "px"; // Abre el contenido
            }
        });
    });
});