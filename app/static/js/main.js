document.addEventListener('DOMContentLoaded', () => {
    const sidebarLinks = document.querySelectorAll('.sidebar-menu a');
    const path = window.location.pathname;
    sidebarLinks.forEach(link => {
        if (path.startsWith(link.getAttribute('href'))) {
            link.classList.add('active');
        }
    });
});
