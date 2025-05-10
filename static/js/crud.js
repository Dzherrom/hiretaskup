document.addEventListener('DOMContentLoaded', function() {
    const inputs = document.querySelectorAll("input, textarea");
    inputs.forEach(input => {
        input.addEventListener("focus", function() {
            if (this.value === this.defaultValue) {
                this.value = "";
            }
        })
    })
});