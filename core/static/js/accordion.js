document.addEventListener("DOMContentLoaded", function () {
        const accordionHeaders = document.querySelectorAll(".accordion-header");

        accordionHeaders.forEach(header => {
            header.addEventListener("click", function () {
                const content = this.nextElementSibling;

                // Alternar la clase "active" para la flecha
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