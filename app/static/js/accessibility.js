// Accessibility Enforcement API
document.addEventListener('DOMContentLoaded', () => {
    const root = document.body;

    // Strict evaluation against LocalStorage preventing UI-flashes wherever structurally possible.
    if (localStorage.getItem('a11y-high-contrast') === 'true') {
        root.classList.add('high-contrast');
    }
    if (localStorage.getItem('a11y-text-large') === 'true') {
        root.classList.add('text-large');
    }

    // Attach listeners strictly verifying button existence
    const contrastBtn = document.getElementById('a11y-contrast-toggle');
    const textBtn = document.getElementById('a11y-text-toggle');

    if (contrastBtn) {
        contrastBtn.addEventListener('click', () => {
            root.classList.toggle('high-contrast');
            localStorage.setItem('a11y-high-contrast', root.classList.contains('high-contrast'));
        });
    }

    if (textBtn) {
        textBtn.addEventListener('click', () => {
            root.classList.toggle('text-large');
            localStorage.setItem('a11y-text-large', root.classList.contains('text-large'));
        });
    }
});
