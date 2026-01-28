document.addEventListener('DOMContentLoaded', function () {
    initThemeToggle();
    initParticles();
    initSmoothScroll();
    initMobileMenu();
    initSkillAnimations();
});

function initThemeToggle() {
    const themeToggle = document.getElementById('theme-toggle');
    if (!themeToggle) return;

    themeToggle.addEventListener('click', function () {
        const currentTheme = document.documentElement.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';

        document.documentElement.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);

        if (window.pJSDom && window.pJSDom.length > 0) {
            updateParticlesTheme(newTheme);
        }
    });
}

function initParticles() {
    const particlesContainer = document.getElementById('particles-js');
    if (!particlesContainer) return;

    const theme = document.documentElement.getAttribute('data-theme');
    const particleColor = theme === 'light' ? '#ea580c' : '#f97316';
    const lineColor = theme === 'light' ? '#0d9488' : '#14b8a6';

    tsParticles.load('particles-js', {
        particles: {
            number: {
                value: 60,
                density: {
                    enable: true,
                    area: 800
                }
            },
            color: {
                value: [particleColor, lineColor]
            },
            shape: {
                type: 'circle'
            },
            opacity: {
                value: 0.5,
                random: true,
                animation: {
                    enable: true,
                    speed: 1,
                    minimumValue: 0.1,
                    sync: false
                }
            },
            size: {
                value: 3,
                random: true,
                animation: {
                    enable: true,
                    speed: 2,
                    minimumValue: 0.5,
                    sync: false
                }
            },
            links: {
                enable: true,
                distance: 150,
                color: lineColor,
                opacity: 0.3,
                width: 1
            },
            move: {
                enable: true,
                speed: 1,
                direction: 'none',
                random: false,
                straight: false,
                outModes: {
                    default: 'bounce'
                },
                attract: {
                    enable: false,
                    rotateX: 600,
                    rotateY: 1200
                }
            }
        },
        interactivity: {
            detectsOn: 'canvas',
            events: {
                onHover: {
                    enable: true,
                    mode: 'grab'
                },
                onClick: {
                    enable: true,
                    mode: 'push'
                },
                resize: true
            },
            modes: {
                grab: {
                    distance: 140,
                    links: {
                        opacity: 0.5
                    }
                },
                push: {
                    quantity: 4
                }
            }
        },
        background: {
            color: 'transparent'
        },
        detectRetina: true
    });
}

function updateParticlesTheme(theme) {
    const particleColor = theme === 'light' ? '#ea580c' : '#f97316';
    const lineColor = theme === 'light' ? '#0d9488' : '#14b8a6';

    const container = tsParticles.domItem(0);
    if (container) {
        container.options.particles.color.value = [particleColor, lineColor];
        container.options.particles.links.color = lineColor;
        container.refresh();
    }
}

function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                const headerOffset = 80;
                const elementPosition = target.getBoundingClientRect().top;
                const offsetPosition = elementPosition + window.pageYOffset - headerOffset;

                window.scrollTo({
                    top: offsetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });
}

function initMobileMenu() {
    const mobileToggle = document.getElementById('mobile-menu-toggle');
    const navLinks = document.querySelector('.nav-links');

    if (!mobileToggle || !navLinks) return;

    mobileToggle.addEventListener('click', function () {
        navLinks.classList.toggle('active');
        mobileToggle.classList.toggle('active');
    });

    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', () => {
            navLinks.classList.remove('active');
            mobileToggle.classList.remove('active');
        });
    });
}

function initSkillAnimations() {
    const skillBars = document.querySelectorAll('.skill-progress');

    if (skillBars.length === 0) return;

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.width = entry.target.style.getPropertyValue('--progress');
                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.5
    });

    skillBars.forEach(bar => {
        bar.style.width = '0';
        observer.observe(bar);
    });
}

document.addEventListener('scroll', function () {
    const header = document.querySelector('.site-header');
    if (!header) return;

    if (window.scrollY > 50) {
        header.classList.add('scrolled');
    } else {
        header.classList.remove('scrolled');
    }
});
