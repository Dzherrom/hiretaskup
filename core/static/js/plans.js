document.addEventListener('DOMContentLoaded', function() {
    const btn = document.getElementById('choosePlanBtn');
    const dropdown = document.getElementById('choosePlanDropdown');

    btn.addEventListener('click', function(e) {
        e.preventDefault();
        dropdown.classList.toggle('active');
    });

    // Close dropdown when clicking outside
    document.addEventListener('click', function(e) {
        if (!btn.contains(e.target) && !dropdown.contains(e.target)) {
            dropdown.classList.remove('active');
        }
    });
});