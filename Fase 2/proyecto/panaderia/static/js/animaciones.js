// IIFE para evitar contaminación del scope global
(function() {
    // Función para inicializar el carrusel
    function initializeCarousel() {
        try {
            if (typeof bootstrap !== 'undefined') {
                const carousel = document.querySelector('#carouselExampleAutoplaying');
                if (carousel) {
                    new bootstrap.Carousel(carousel, {
                        interval: 3000,
                        wrap: true
                    });
                }
            }
        } catch (error) {
            console.warn('Error initializing carousel:', error);
        }
    }

    // Función para manejar las animaciones de aparición
    function initializeFadeAnimations() {
        try {
            const observerOptions = {
                threshold: 0.2,
                rootMargin: '50px'
            };

            const fadeInObserver = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        entry.target.classList.add('is-visible');
                        
                        // Animar enlaces sociales si existen
                        if (entry.target.classList.contains('contact-item')) {
                            const socialLinks = entry.target.querySelectorAll('.social-link');
                            socialLinks.forEach((link, index) => {
                                link.style.setProperty('--index', index);
                            });
                        }
                    }
                });
            }, observerOptions);

            const animatedElements = document.querySelectorAll(
                '.scroll-reveal, .contact-item, .fade-in-section, .about-image, .about-content'
            );
            
            animatedElements.forEach(element => {
                fadeInObserver.observe(element);
            });

            console.log('Fade animations initialized with', animatedElements.length, 'elements');
        } catch (error) {
            console.warn('Error initializing fade animations:', error);
        }
    }

    // Función para manejar la animación del navbar
    function initializeNavbarAnimation() {
        try {
            const navbar = document.querySelector('.navbar');
            if (!navbar) return;

            let lastScrollTop = 0;
            let ticking = false;

            window.addEventListener('scroll', function() {
                if (!ticking) {
                    window.requestAnimationFrame(function() {
                        const currentScroll = window.pageYOffset || document.documentElement.scrollTop;
                        
                        if (currentScroll > lastScrollTop && currentScroll > 100) {
                            navbar.style.top = '-100px';
                        } else {
                            navbar.style.top = '0';
                        }
                        
                        lastScrollTop = currentScroll <= 0 ? 0 : currentScroll;
                        ticking = false;
                    });
                    ticking = true;
                }
            }, { passive: true });
        } catch (error) {
            console.warn('Error initializing navbar animation:', error);
        }
    }

    // Función para manejar la animación del botón toggler
    function initializeTogglerAnimation() {
        try {
            const navbarToggler = document.querySelector('.navbar-toggler');
            if (navbarToggler) {
                navbarToggler.addEventListener('click', function() {
                    this.classList.toggle('active');
                });
            }
        } catch (error) {
            console.warn('Error initializing toggler animation:', error);
        }
    }

    // Función principal de inicialización
    function initialize() {
        // Cada función se ejecuta independientemente
        initializeCarousel();
        initializeFadeAnimations();
        initializeNavbarAnimation();
        initializeTogglerAnimation();
    }

    // Event listener para DOMContentLoaded
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initialize);
    } else {
        initialize();
    }
})();