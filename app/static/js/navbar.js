/**
 * Navbar - Sistema de navegación global
 */

document.addEventListener('DOMContentLoaded', function() {
    const navbar = document.querySelector('.navbar');
    const navbarToggle = document.querySelector('.navbar-toggle');
    const navbarMenu = document.querySelector('.navbar-menu');
    const navbarOverlay = document.querySelector('.navbar-overlay');
    const navbarLinks = document.querySelectorAll('.navbar-nav-link');

    // Efecto scroll en navbar
    let lastScroll = 0;
    window.addEventListener('scroll', function() {
        const currentScroll = window.pageYOffset;

        if (currentScroll > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }

        lastScroll = currentScroll;
    });

    // Toggle menu móvil
    if (navbarToggle) {
        navbarToggle.addEventListener('click', function() {
            navbarToggle.classList.toggle('active');
            navbarMenu.classList.toggle('active');
            navbarOverlay.classList.toggle('active');
            document.body.style.overflow = navbarMenu.classList.contains('active') ? 'hidden' : '';
        });
    }

    // Cerrar menu al hacer click en overlay
    if (navbarOverlay) {
        navbarOverlay.addEventListener('click', function() {
            navbarToggle.classList.remove('active');
            navbarMenu.classList.remove('active');
            navbarOverlay.classList.remove('active');
            document.body.style.overflow = '';
        });
    }

    // Cerrar menu al hacer click en un link
    navbarLinks.forEach(link => {
        link.addEventListener('click', function() {
            if (window.innerWidth <= 968) {
                navbarToggle.classList.remove('active');
                navbarMenu.classList.remove('active');
                navbarOverlay.classList.remove('active');
                document.body.style.overflow = '';
            }
        });
    });

    // Marcar link activo basado en URL actual
    const currentPath = window.location.pathname;
    navbarLinks.forEach(link => {
        const linkPath = new URL(link.href).pathname;
        if (linkPath === currentPath) {
            link.classList.add('active');
        }
    });

    // Cerrar menu al redimensionar ventana
    window.addEventListener('resize', function() {
        if (window.innerWidth > 968) {
            navbarToggle.classList.remove('active');
            navbarMenu.classList.remove('active');
            navbarOverlay.classList.remove('active');
            document.body.style.overflow = '';
        }
    });
});
