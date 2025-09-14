document.addEventListener("DOMContentLoaded", function () {
    const slider = document.querySelector(".reviews-slider");
    const leftArrow = document.querySelector(".left-arrow");
    const rightArrow = document.querySelector(".right-arrow");
    let isDown = false;
    let startX;
    let scrollLeft;

    leftArrow.addEventListener("click", () => {
        slider.scrollBy({ left: -300, behavior: "smooth" }); // Desplaza hacia la izquierda
    });

    rightArrow.addEventListener("click", () => {
        slider.scrollBy({ left: 300, behavior: "smooth" }); // Desplaza hacia la derecha
    });
    
    // Evento al presionar el mouse
    slider.addEventListener("mousedown", (e) => {
        isDown = true;
        slider.classList.add("active");
        startX = e.pageX - slider.offsetLeft;
        scrollLeft = slider.scrollLeft;
    });

    // Evento al salir del área del slider
    slider.addEventListener("mouseleave", () => {
        isDown = false;
        slider.classList.remove("active");
    });

    // Evento al soltar el mouse
    slider.addEventListener("mouseup", () => {
        isDown = false;
        slider.classList.remove("active");
    });

    // Evento al mover el mouse
    slider.addEventListener("mousemove", (e) => {
        if (!isDown) return; // Si no se está presionando, no hacer nada
        e.preventDefault();
        const x = e.pageX - slider.offsetLeft;
        const walk = (x - startX) * 2; // Ajusta la velocidad del desplazamiento
        slider.scrollLeft = scrollLeft - walk;
    });
});