document.addEventListener('submit', event => {
    const form = event.target;
    if (form.matches('.auth-form, .form-grid')) {
        form.querySelectorAll('button[type="submit"]').forEach(btn => {
            btn.disabled = true;
            btn.textContent = 'جاري المعالجة...';
        });
    }
});
