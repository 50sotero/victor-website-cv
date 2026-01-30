import { animate, inView, stagger, spring } from "https://cdn.jsdelivr.net/npm/motion@10.17.0/+esm";

document.addEventListener('DOMContentLoaded', function () {
    // We can keep these non-animation initialization functions
    initThemeToggle();
    initParticles();
    initSmoothScroll();
    initMobileMenu();

    // New Motion One Animations
    initHeroAnimations();
    initScrollAnimations();
    initSkillAnimations(); // Refactored
    initHoverEffects();

    // Keep the cursor effect
    initCursorEffect();
});

function initHeroAnimations() {
    // Animate Hero Content (Title, Subtitle, Buttons)
    // Assuming the hero section is in 'main' or has specific classes. 
    // If specific classes aren't there, we might need to target generic elements, 
    // but typically a hero has h1, p, and buttons.

    // Let's try to target the first section's content if specific classes are missing,
    // or we can strictly target `.hero-content > *` if that class exists.
    // Based on standard Hugo themes or common structures:
    const heroElements = document.querySelectorAll('main section:first-of-type > *');

    if (heroElements.length > 0) {
        animate(
            heroElements,
            { opacity: [0, 1], y: [50, 0] },
            {
                duration: 0.8,
                delay: stagger(0.2),
                easing: "ease-out"
            }
        );
    }
}

function initScrollAnimations() {
    // General Fade-in/Slide-up for sections as they scroll into view
    inView("section:not(:first-of-type)", ({ target }) => {
        animate(
            target,
            { opacity: [0, 1], transform: ["translateY(50px)", "none"] },
            { duration: 0.6, easing: "ease-out" }
        );
    });

    // Floating Icons Global - Staggered entrance
    // The previous CSS animation might be conflicting or we can enhance it.
    // If they have distinct classes, we can animate their entrance initially.
    const floatingIcons = document.querySelectorAll('.floating-icon');
    if (floatingIcons.length > 0) {
        animate(
            floatingIcons,
            { opacity: [0, 1], scale: [0, 1] },
            {
                duration: 0.5,
                delay: stagger(0.1, { start: 0.5 }),
                easing: spring()
            }
        );
        // Note: The CSS 'float' animation will continue to run if it's keyframe based.
    }
}

function initSkillAnimations() {
    // Refactored to use Motion One
    const skillBars = document.querySelectorAll('.skill-progress');

    // Using inView for scroll triggering
    inView('.skill-progress', ({ target }) => {
        const progress = target.style.getPropertyValue('--progress') || '100%';

        animate(
            target,
            { width: [0, progress] },
            {
                duration: 1.2,
                easing: spring({ stiffness: 50, damping: 10 })
            }
        );
    });
}

function initHoverEffects() {
    // Add spring scale effect to cards or buttons
    const interactiveElements = document.querySelectorAll('.btn, .project-card, .floating-icon');

    interactiveElements.forEach(el => {
        el.addEventListener('mouseenter', () => {
            animate(el, { scale: 1.05 }, { duration: 0.3, easing: spring() });
        });

        el.addEventListener('mouseleave', () => {
            animate(el, { scale: 1 }, { duration: 0.3, easing: spring() });
        });
    });
}

// --- Specific Initializers (kept mostly same but cleaned up) ---

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

    if (typeof tsParticles === 'undefined') return;

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
                value: 0.7,
                random: true,
                animation: {
                    enable: true,
                    speed: 1,
                    minimumValue: 0.3,
                    sync: false
                }
            },
            size: {
                value: 4,
                random: true,
                animation: {
                    enable: true,
                    speed: 2,
                    minimumValue: 1,
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
            detectsOn: 'window',
            events: {
                onHover: {
                    enable: true,
                    mode: 'grab' // Fixed from 'item'
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
                    quantity: 8 // Double quantity for better visibility
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

document.addEventListener('scroll', function () {
    const header = document.querySelector('.site-header');
    if (!header) return;

    if (window.scrollY > 50) {
        header.classList.add('scrolled');
    } else {
        header.classList.remove('scrolled');
    }
});

function initCursorEffect() {
    const cursorArea = document.getElementById('cursor-area');
    if (!cursorArea) return;

    document.addEventListener('pointermove', (event) => {
        const xPercent = (event.clientX / window.innerWidth) * 100;
        const yPercent = (event.clientY / window.innerHeight) * 100;
        document.documentElement.style.setProperty('--ring-x', xPercent);
        document.documentElement.style.setProperty('--ring-y', yPercent);
    });

    document.addEventListener('pointerleave', () => {
        document.documentElement.style.setProperty('--particle-max-alpha', 0);
    });

    document.addEventListener('pointerenter', () => {
        document.documentElement.style.setProperty('--particle-max-alpha', 1);
    });

    let tick = 0;
    function animateCursor() {
        tick += 1;
        document.documentElement.style.setProperty('--animation-tick', tick);
        requestAnimationFrame(animateCursor);
    }
    animateCursor();
}
