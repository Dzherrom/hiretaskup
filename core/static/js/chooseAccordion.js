document.addEventListener("DOMContentLoaded", function() {
    const accordionItems = document.querySelectorAll(".choose-card .accordion-item");

    accordionItems.forEach(item => {
        const header = item.querySelector(".accordion-header");
        const content = item.querySelector(".accordion-content");

        header.addEventListener("click", function() {
            const isOpen = item.classList.contains("active");

            // Cierra todos los items
            accordionItems.forEach(i => {
                i.classList.remove("active");
                i.querySelector(".accordion-content").style.maxHeight = null;
            });

            // Si no estaba abierto, ábrelo
            if (!isOpen) {
                item.classList.add("active");
                content.style.maxHeight = content.scrollHeight + "px";
            }
        });
    });
    
    const slider = document.querySelector(".reviews-slider");
    const leftArrow = document.querySelector(".left-arrow");
    const rightArrow = document.querySelector(".right-arrow");

    leftArrow.addEventListener("click", () => {
        slider.scrollBy({ left: -300, behavior: "smooth" });
    });

    rightArrow.addEventListener("click", () => {
        slider.scrollBy({ left: 300, behavior: "smooth" });
    });
});