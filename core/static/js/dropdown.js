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

// Mobile Menu Logic
document.addEventListener('DOMContentLoaded', () => {
    const mobileToggle = document.getElementById('mobileMenuToggle');
    const mobileOverlay = document.getElementById('mobileMenuOverlay');
    const mobileClose = document.getElementById('mobileMenuClose');

    const closeMenu = () => {
        if (mobileOverlay) {
            mobileOverlay.classList.remove('open');
            document.body.style.overflow = 'auto'; // Restore scrolling
        }
    };

    if (mobileToggle && mobileOverlay && mobileClose) {
        mobileToggle.addEventListener('click', () => {
            // Add class instead of setting style to trigger CSS transition
            mobileOverlay.classList.add('open'); 
            document.body.style.overflow = 'hidden'; // Prevent scrolling
            if (window.lucide) {
                lucide.createIcons(); // Re-render icons if needed
            }
        });

        mobileClose.addEventListener('click', closeMenu);

        // Close menu if window is resized larger than 1000px
        window.addEventListener('resize', () => {
            if (window.innerWidth > 1000) {
                closeMenu();
            }
        });
    }
});