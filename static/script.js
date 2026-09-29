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

    const openInboxBtn = document.getElementById('openInboxBtn');
    const closeInboxBtn = document.getElementById('closeInboxBtn');
    const inboxModal = document.getElementById('inboxModal');
    const messagesList = document.getElementById('messagesList');
    const msgCountBadge = document.getElementById('msgCountBadge');

    // 1. Character Counter for Message Box
    messageInput.addEventListener('input', () => {
        charNum.textContent = messageInput.value.length;
    });

    // 2. Fetch Stored Message Count on Load
    fetchStoredMessagesCount();

    // 3. Form Submit Handler
    contactForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        // Reset previous errors
        resetErrors();

        // Simple validation
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
                fetchStoredMessagesCount();
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

    // Helper functions for Form
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

    // 4. Stored DB Messages Inbox Modal Logic
    openInboxBtn.addEventListener('click', () => {
        inboxModal.classList.add('active');
        loadMessagesIntoModal();
    });

    closeInboxBtn.addEventListener('click', () => {
        inboxModal.classList.remove('active');
    });

    inboxModal.addEventListener('click', (e) => {
        if (e.target === inboxModal) {
            inboxModal.classList.remove('active');
        }
    });

    async function fetchStoredMessagesCount() {
        try {
            const res = await fetch('/api/messages');
            if (res.ok) {
                const data = await res.json();
                if (msgCountBadge) {
                    msgCountBadge.textContent = data.count || '0';
                }
            }
        } catch (e) {
            console.error("Could not fetch messages count:", e);
        }
    }

    async function loadMessagesIntoModal() {
        messagesList.innerHTML = `<div class="loading-state"><i class="fa-solid fa-circle-notch fa-spin"></i> Fetching records from database...</div>`;
        try {
            const res = await fetch('/api/messages');
            if (res.ok) {
                const data = await res.json();
                renderMessagesList(data.messages || []);
            } else {
                messagesList.innerHTML = `<div class="alert-box alert-error">Failed to load messages from server.</div>`;
            }
        } catch (err) {
            messagesList.innerHTML = `<div class="alert-box alert-error">Network error when accessing database API.</div>`;
        }
    }

    function renderMessagesList(messages) {
        if (messages.length === 0) {
            messagesList.innerHTML = `
                <div style="text-align: center; padding: 40px 20px; color: var(--text-muted);">
                    <i class="fa-solid fa-inbox" style="font-size: 2.5rem; color: var(--text-dim); margin-bottom: 12px;"></i>
                    <p>No messages stored in the database yet.</p>
                    <p style="font-size: 0.8rem; color: var(--text-dim);">Submit the contact form on the portfolio to create your first entry!</p>
                </div>
            `;
            return;
        }

        messagesList.innerHTML = messages.map(msg => `
            <div class="msg-card">
                <div class="msg-card-header">
                    <div>
                        <span class="msg-author">${escapeHtml(msg.name)}</span>
                        &lt;<a class="msg-email" href="mailto:${escapeHtml(msg.email)}">${escapeHtml(msg.email)}</a>&gt;
                    </div>
                    <div class="msg-date"><i class="fa-regular fa-clock"></i> ${escapeHtml(msg.created_at)}</div>
                </div>
                <div class="msg-subject">📌 ${escapeHtml(msg.subject)}</div>
                <div class="msg-content">${escapeHtml(msg.message)}</div>
                <div class="msg-footer">
                    <span>IP: ${escapeHtml(msg.ip_address || '127.0.0.1')}</span>
                    <span class="badge-notified"><i class="fa-solid fa-circle-check"></i> ${msg.notified_via_email ? 'Emailed' : 'Stored in DB (Preview Mode)'}</span>
                </div>
            </div>
        `).join('');
    }

    function escapeHtml(str) {
        if (!str) return '';
        return String(str)
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }
});
