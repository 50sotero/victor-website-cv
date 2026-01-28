// Ring Particles Cursor Effect - JavaScript
// Tracks pointer position and updates CSS custom properties for the paint worklet

(function () {
    'use strict';

    // Update ring position based on pointer movement
    document.addEventListener('pointermove', (event) => {
        const xPercent = (event.clientX / window.innerWidth) * 100;
        const yPercent = (event.clientY / window.innerHeight) * 100;

        document.documentElement.style.setProperty('--ring-x', xPercent);
        document.documentElement.style.setProperty('--ring-y', yPercent);
    });

    // Hide ring when pointer leaves the viewport
    document.addEventListener('pointerleave', () => {
        document.documentElement.style.setProperty('--particle-max-alpha', '0');
    });

    // Show ring when pointer enters the viewport
    document.addEventListener('pointerenter', () => {
        const theme = document.documentElement.getAttribute('data-theme');
        const alpha = theme === 'light' ? '0.6' : '0.8';
        document.documentElement.style.setProperty('--particle-max-alpha', alpha);
    });

    // Optional: Animate the ring with a pulsating effect
    let tick = 0;
    function animateRing() {
        tick = (tick + 1) % 360;
        document.documentElement.style.setProperty('--animation-tick', tick);
        requestAnimationFrame(animateRing);
    }

    // Start animation when page loads
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', animateRing);
    } else {
        animateRing();
    }
})();
