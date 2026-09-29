document.addEventListener('DOMContentLoaded', () => {
    const contactForm = document.getElementById('contactForm');
    const nameInput = document.getElementById('name');
    const emailInput = document.getElementById('email');
    const subjectInput = document.getElementById('subject');
    const messageInput = document.getElementById('message');
    const charNum = document.getElementById('charNum');

    const submitBtn = document.getElementById('submitBtn');
    const btnText = submitBtn.querySelector('.btn-text');
    const btnSpinner = document.getElementById('btnSpinner');
    const alertBox = document.getElementById('alertBox');

    // 1. Character Counter for Message Box
    messageInput.addEventListener('input', () => {
        charNum.textContent = messageInput.value.length;
    });

    // 2. Form Submit Handler
    contactForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        // Reset previous errors
        resetErrors();

        // Input validation
        let isValid = true;
        if (!nameInput.value.trim() || nameInput.value.trim().length < 2) {
            showError('nameError', 'Please enter your name (min 2 characters)');
            isValid = false;
        }

        if (!emailInput.value.trim() || !validateEmail(emailInput.value.trim())) {
            showError('emailError', 'Please enter a valid email address');
            isValid = false;
        }

        if (!subjectInput.value.trim()) {
            showError('subjectError', 'Please enter a subject');
            isValid = false;
        }

        if (!messageInput.value.trim() || messageInput.value.trim().length < 5) {
            showError('messageError', 'Please enter your message (min 5 characters)');
            isValid = false;
        }

        if (!isValid) return;

        // Set Loading UI state
        setLoadingState(true);

        const payload = {
            name: nameInput.value.trim(),
            email: emailInput.value.trim(),
            subject: subjectInput.value.trim(),
            message: messageInput.value.trim()
        };

        try {
            const response = await fetch('/api/contact', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(payload)
            });

            const data = await response.json();

            if (response.ok && data.success) {
                showAlert('success', `<i class="fa-solid fa-circle-check"></i> ${data.message}`);
                contactForm.reset();
                charNum.textContent = '0';
            } else {
                const errDetail = data.detail ? (typeof data.detail === 'string' ? data.detail : JSON.stringify(data.detail)) : 'Failed to submit form';
                showAlert('error', `<i class="fa-solid fa-triangle-exclamation"></i> Error: ${errDetail}`);
            }
        } catch (err) {
            showAlert('error', `<i class="fa-solid fa-wifi"></i> Network error: Could not reach the backend server.`);
        } finally {
            setLoadingState(false);
        }
    });

    // Helper functions
    function validateEmail(email) {
        return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
    }

    function showError(elementId, text) {
        const el = document.getElementById(elementId);
        if (el) {
            el.textContent = text;
            el.style.display = 'block';
        }
    }

    function resetErrors() {
        document.querySelectorAll('.error-msg').forEach(el => el.style.display = 'none');
        alertBox.style.display = 'none';
        alertBox.className = 'alert-box';
    }

    function showAlert(type, htmlContent) {
        alertBox.innerHTML = htmlContent;
        alertBox.className = `alert-box alert-${type}`;
        alertBox.style.display = 'block';
    }

    function setLoadingState(isLoading) {
        if (isLoading) {
            submitBtn.disabled = true;
            btnText.style.display = 'none';
            btnSpinner.style.display = 'inline-block';
        } else {
            submitBtn.disabled = false;
            btnText.style.display = 'inline-block';
            btnSpinner.style.display = 'none';
        }
    }
});
