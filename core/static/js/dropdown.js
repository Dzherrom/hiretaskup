const toggle = document.getElementById('userDropdownToggle');
const menu = document.getElementById('userDropdownMenu');
document.addEventListener('click', function(event) {
    if (toggle.contains(event.target)) {
        event.preventDefault();
        menu.style.display = menu.style.display === 'block' ? 'none' : 'block';
    } else if (!menu.contains(event.target)) {
        menu.style.display = 'none';
    }
});