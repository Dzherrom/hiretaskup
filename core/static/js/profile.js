document.addEventListener('DOMContentLoaded', function() {
    const fields = [
        {id: 'id_first_name', defaultValue: 'No First Name'},
        {id: 'id_last_name', defaultValue: 'No Last Name'},
        {id: 'id_address', defaultValue: 'No Address'},
        {id: 'id_email', defaultValue: 'you@email.com'}
    ];
    fields.forEach(function(fieldObj) {
        const field = document.getElementById(fieldObj.id);
        if (field) {
            field.addEventListener('focus', function handler() {
                if (field.value === fieldObj.defaultValue) {
                    field.value = '';
                }
                field.removeEventListener('focus', handler);
            });
        }
    });
});

document.addEventListener('DOMContentLoaded', function() {
    // Solo permitir números en el campo phone_number
    const phoneInput = document.getElementById('id_phone_number');
    if (phoneInput) {
        phoneInput.addEventListener('input', function() {
            this.value = this.value.replace(/\D/g, '');
        });
    }

    // Cambiar la longitud máxima según el país seleccionado
    const countryInput = document.getElementById('id_country');
    if (countryInput && phoneInput) {
        const phoneLengths = {
            'co': 10, // Colombia
            'mx': 10, // México
            'ar': 10  // Argentina (ajusta según el país)
        };
        function updatePhoneLength() {
            const selected = countryInput.value;
            phoneInput.maxLength = phoneLengths[selected] || 10;
        }
        countryInput.addEventListener('change', updatePhoneLength);
        updatePhoneLength(); // Inicializa al cargar la página
    }
});