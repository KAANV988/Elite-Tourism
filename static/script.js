// --- Mobile Menu Toggle ---
const menuButton = document.getElementById('mobile-menu-button');
const mobileMenu = document.getElementById('mobile-menu');

menuButton.addEventListener('click', () => {
    mobileMenu.classList.toggle('hidden');
});

// Close mobile menu when a link is clicked
mobileMenu.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', () => {
        mobileMenu.classList.add('hidden');
    });
});

// --- Navbar Style on Scroll ---
const navbar = document.getElementById('navbar');
window.addEventListener('scroll', () => {
    if (window.scrollY > 50) {
        // Already handled by navbar-glass, but you could add more effects
        // e.g., navbar.classList.add('shadow-lg');
    } else {
        // navbar.classList.remove('shadow-lg');
    }
});

// --- Footer: Current Year ---
document.getElementById('current-year').textContent = new Date().getFullYear();

// --- Fade-in Sections on Scroll ---
const sections = document.querySelectorAll('.fade-in-section');

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('is-visible');
            // Optional: unobserve after it has faded in
            // observer.unobserve(entry.target); 
        }
    });
}, {
    threshold: 0.1 // Trigger when 10% of the section is visible
});

sections.forEach(section => {
    observer.observe(section);
});