document.addEventListener('DOMContentLoaded', function() {
    // Lista de zonas horarias comunes (puedes ajustar según tus necesidades)
const commonTimezones = [
    "America/New_York", "America/Chicago", "America/Denver", "America/Los_Angeles",
    "America/Mexico_City", "America/Bogota", "America/Lima", "America/Sao_Paulo",
    "America/Buenos_Aires", "Europe/London", "Europe/Madrid", "Europe/Paris",
    "Europe/Berlin", "Europe/Rome", "Europe/Moscow", "Europe/Istanbul",
    "Asia/Dubai", "Asia/Kolkata", "Asia/Bangkok", "Asia/Singapore",
    "Asia/Tokyo", "Asia/Shanghai", "Asia/Hong_Kong", "Australia/Sydney",
    "Pacific/Auckland"
];

const timezoneSelect = document.getElementById('timezone-select');
if (timezoneSelect) {
    // Limpia opciones previas
    timezoneSelect.innerHTML = '';
    // Agrupa por continente
    const groups = {};
    commonTimezones.forEach(tz => {
        const group = tz.split('/')[0];
        if (!groups[group]) {
            groups[group] = [];
        }
        groups[group].push(tz);
    });
    Object.keys(groups).forEach(group => {
        const optgroup = document.createElement('optgroup');
        optgroup.label = group;
        groups[group].forEach(tz => {
            const option = document.createElement('option');
            option.value = tz;
            option.text = tz.replace(/_/g, ' ');
            optgroup.appendChild(option);
        });
        timezoneSelect.appendChild(optgroup);
    });

    // Inicializa Select2
    $('#timezone-select').select2({
        placeholder: "Select a time zone",
        allowClear: true,
        width: 'resolve'
    });

    // Selecciona automáticamente la zona horaria local del usuario si está en la lista
    const localTz = Intl.DateTimeFormat().resolvedOptions().timeZone;
    if (commonTimezones.includes(localTz)) {
        $('#timezone-select').val(localTz).trigger('change');
    }
}

    // Inicializa flatpickr
    flatpickr("#calendar", {
        inline: true,
        minDate: "today",
        maxDate: new Date(Date.now() + 21 * 24 * 60 * 60 * 1000), // 21 días desde hoy
        locale: { firstDayOfWeek: 1 },
        monthSelectorType: "static",
        onChange: function(selectedDates, dateStr, instance) {
            if (selectedDates.length > 0) {
                showTimeSelection(selectedDates[0]);
            }
        },
        onReady: function(selectedDates, dateStr, instance) {
            showYearAsText(instance);
        },
        onMonthChange: function(selectedDates, dateStr, instance) {
            showYearAsText(instance);
        }
    });

function showYearAsText(instance) {
    const monthContainer = instance.calendarContainer.querySelector('.flatpickr-current-month');
    if (!monthContainer) return;
    // Elimina cualquier año plano previo
    const prev = monthContainer.querySelector('.year-plain');
    if (prev) prev.remove();
    // Obtiene el año actual
    const year = instance.currentYear;
    // Crea el span de año plano
    const yearSpan = document.createElement('span');
    yearSpan.className = 'year-plain';
    yearSpan.textContent = ' ' + year;
    yearSpan.style.fontSize = '1.1rem';
    yearSpan.style.fontWeight = '600';
    yearSpan.style.color = '#006aff';
    yearSpan.style.marginLeft = '2px';
    // Inserta después del mes
    const curMonth = monthContainer.querySelector('.cur-month');
    if (curMonth) curMonth.after(yearSpan);
}

    const calendarCard = document.querySelector('.calendar-card');
    const timeSelectionCard = document.getElementById('timeSelectionCard');
    const backBtn = document.getElementById('backToCalendar');

    const phoneInput = document.querySelector("#phoneInput");
    const itiPhone = window.intlTelInput(phoneInput, {
        initialCountry: "auto",
        geoIpLookup: function(callback) {
        fetch('https://ipinfo.io/json?token=<6db1cea8941122>')
            .then((resp) => resp.json())
            .then((resp) => callback(resp.country ? resp.country : "us"))
            .catch(() => callback("us"));
        },
        preferredCountries: ["us", "gb", "co", "mx"],
        utilsScript: "https://cdn.jsdelivr.net/npm/intl-tel-input@18.1.1/build/js/utils.js"
    });

    function showTimeSelection(dateObj) {
        // Oculta el calendario y muestra la selección de hora
        calendarCard.style.display = 'none';
        timeSelectionCard.style.display = 'block';

        // Muestra el día y la fecha seleccionada
        const dayNames = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'];
        document.getElementById('selectedDay').textContent = dayNames[dateObj.getDay()];
        document.getElementById('selectedDate').textContent = dateObj.toLocaleDateString('en-US', {
            year: 'numeric', month: 'long', day: 'numeric'
        });

        // Muestra el timezone seleccionado
        document.getElementById('selectedTimezone').textContent = timezoneSelect.options[timezoneSelect.selectedIndex].text;

        // Genera los horarios de 14:00 a 23:45 cada 15 minutos
        const slotsContainer = document.getElementById('timeSlots');
        slotsContainer.innerHTML = '';
        let start = new Date(dateObj);
        start.setHours(14,0,0,0);
        for(let h=14; h<=23; h++) {
            for(let m=0; m<60; m+=15) {
                if(h === 23 && m > 45) break;
                let slot = new Date(dateObj);
                slot.setHours(h, m, 0, 0);
                let label = slot.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit', hour12: false});
                let btn = document.createElement('button');
                btn.className = 'time-slot-btn';
                btn.textContent = label;
                slotsContainer.appendChild(btn);
            }
        }
        let selectedSlot = null;
        function renderTimeSlots(selectedLabel = null) {
            slotsContainer.innerHTML = '';
            for(let h=14; h<=23; h++) {
                for(let m=0; m<60; m+=15) {
                    if(h === 23 && m > 45) break;
                    let slot = new Date(dateObj);
                    slot.setHours(h, m, 0, 0);
                    let label = slot.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit', hour12: false});

                    let slotWrapper = document.createElement('div');
                    slotWrapper.style.display = 'flex';
                    slotWrapper.style.gap = '8px';
                    slotWrapper.style.justifyContent = 'center';

                    let btn = document.createElement('button');
                    btn.className = 'time-slot-btn';
                    btn.textContent = label;

                    if (selectedLabel === label) {
                        btn.classList.add('selected');
                        btn.style.background = '#666';
                        btn.style.color = '#fff';
                        btn.style.flex = '1';
                        // Botón Next
                        let nextBtn = document.createElement('button');
                        nextBtn.className = 'next-btn';
                        nextBtn.textContent = 'Next';
                        nextBtn.style.flex = '1';
                        nextBtn.onclick = function() {
                            // Mostrar formulario de confirmación
                            document.getElementById('timeSelectionCard').style.display = 'none';
                            document.getElementById('confirmationFormCard').style.display = 'block';
                            // Rellenar resumen
                            document.getElementById('summaryTime').textContent =
                                label + ' - ' +
                                addMinutesToLabel(label, 20) + ', ' +
                                document.getElementById('selectedDay').textContent + ', ' +
                                document.getElementById('selectedDate').textContent;
                                document.getElementById('summaryTimezone').textContent =
                                document.getElementById('selectedTimezone').textContent;
                        };
                        slotWrapper.appendChild(btn);
                        slotWrapper.appendChild(nextBtn);
                    } else {
                        btn.onclick = function() {
                            selectedSlot = label;
                            renderTimeSlots(label);
                        };
                        btn.style.flex = '2';
                        slotWrapper.appendChild(btn);
                    }
                    slotsContainer.appendChild(slotWrapper);
                }
            }
            document.getElementById('backToTimeSelection').onclick = function() {
        document.getElementById('confirmationFormCard').style.display = 'none';
        document.getElementById('timeSelectionCard').style.display = 'block';
    };
    }

        // Renderiza los horarios
        renderTimeSlots();
    }

// Función auxiliar para sumar minutos a la hora seleccionada
function addMinutesToLabel(label, minutes) {
    let [h, m] = label.split(':').map(Number);
    let d = new Date();
    d.setHours(h, m + minutes, 0, 0);
    return d.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit', hour12: false});
}

    // Volver al calendario
    backBtn.addEventListener('click', function() {
        timeSelectionCard.style.display = 'none';
        calendarCard.style.display = 'block';
    });

    // Si cambia el timezone, actualiza el texto en la vista de hora si está visible
    timezoneSelect.addEventListener('change', function() {
        if(timeSelectionCard.style.display === 'block') {
            document.getElementById('selectedTimezone').textContent = timezoneSelect.options[timezoneSelect.selectedIndex].text;
        }
    });

    // Mostrar campo de invitados al hacer click en Add Guests
    document.getElementById('addGuestsBtn').onclick = function() {
        document.getElementById('guestsField').style.display = 'block';
        this.style.display = 'none';
    };

const descToggle = document.querySelector('.desc-toggle');
const descContent = document.querySelector('.desc-content');

if (descToggle && descContent) {
    // Inicializa cerrado
    descContent.style.overflow = "hidden";
    descContent.style.transition = "max-height 0.4s ease";
    descContent.style.maxHeight = null;

    descToggle.addEventListener('click', function() {
        if (descContent.classList.contains('open')) {
            // Cerrar: primero fija la altura actual, luego colapsa
            descContent.style.maxHeight = descContent.scrollHeight + "px";
            // Forzar repaint y luego colapsar
            setTimeout(() => {
                descContent.style.maxHeight = null;
                descContent.classList.remove('open');
            }, 10);
        } else {
            // Abrir: fija la altura y luego, al terminar la transición, la deja en 'none'
            descContent.classList.add('open');
            descContent.style.maxHeight = descContent.scrollHeight + "px";
        }
    });

    // Limpia max-height al terminar la transición para que el contenido se adapte si cambia de tamaño
    descContent.addEventListener('transitionend', function() {
        if (descContent.classList.contains('open')) {
            descContent.style.maxHeight = 'none';
        }
    });
}

const addGuestsBtn = document.getElementById('addGuestsBtn');
const guestsField = document.getElementById('guestsField');

if (addGuestsBtn && guestsField) {
    // Inicializa cerrado
    guestsField.style.maxHeight = null;
    guestsField.style.overflow = "hidden";
    guestsField.style.transition = "max-height 0.4s ease";

    addGuestsBtn.onclick = function() {
        addGuestsBtn.style.display = 'none';
        guestsField.style.display = 'block';
        guestsField.style.maxHeight = guestsField.scrollHeight + "px";
        guestsField.classList.add('open');
    };

    guestsField.addEventListener('transitionend', function() {
        if (guestsField.classList.contains('open')) {
            guestsField.style.maxHeight = 'none';
        }
    });
}

document.getElementById('hiddenDate').value = document.getElementById('selectedDate').textContent;
document.getElementById('hiddenTime').value = selectedTime;
document.getElementById('hiddenTimezone').value = selectedTimezone;
});