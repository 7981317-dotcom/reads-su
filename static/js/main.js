// ============================================
// Theme Management (Updated for VC.ru Style)
// ============================================
function initTheme() {
    const savedTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', savedTheme);
    updateThemeIcon(savedTheme);
}

function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';

    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    updateThemeIcon(newTheme);
}

function updateThemeIcon(theme) {
    const sunIcon = document.querySelector('.theme-icon-sun');
    const moonIcon = document.querySelector('.theme-icon-moon');

    if (sunIcon && moonIcon) {
        if (theme === 'dark') {
            sunIcon.style.display = 'none';
            moonIcon.style.display = 'block';
        } else {
            sunIcon.style.display = 'block';
            moonIcon.style.display = 'none';
        }
    }

    // Fallback for old theme icon (emoji)
    const themeIcon = document.querySelector('.theme-icon');
    if (themeIcon) {
        themeIcon.textContent = theme === 'dark' ? '☀️' : '🌙';
    }
}

// ============================================
// Login Modal (VC.ru Style)
// ============================================
function openLoginModal() {
    const modal = document.getElementById('loginModal');
    if (modal) {
        modal.style.display = 'flex';
        document.body.style.overflow = 'hidden';
    }
}

function closeLoginModal(event) {
    const modal = document.getElementById('loginModal');
    if (modal && (!event || event.target === modal || event.target.classList.contains('modal-close'))) {
        modal.style.display = 'none';
        document.body.style.overflow = '';

        // Reset to login form when closing
        showLoginForm();
    }
}

// Toggle between login and password reset forms
function showPasswordReset(event) {
    if (event) event.preventDefault();

    document.getElementById('loginFormContainer').style.display = 'none';
    document.getElementById('passwordResetContainer').style.display = 'block';
    document.getElementById('passwordResetSuccess').style.display = 'none';

    // Focus on email input
    setTimeout(() => {
        const emailInput = document.getElementById('id_reset_email');
        if (emailInput) emailInput.focus();
    }, 100);
}

function showLoginForm(event) {
    if (event) event.preventDefault();

    document.getElementById('loginFormContainer').style.display = 'block';
    document.getElementById('passwordResetContainer').style.display = 'none';
    document.getElementById('registerFormContainer').style.display = 'none';
    document.getElementById('passwordResetSuccess').style.display = 'none';

    // Clear forms
    const resetForm = document.getElementById('passwordResetForm');
    if (resetForm) resetForm.reset();

    const registerForm = document.getElementById('registerForm');
    if (registerForm) registerForm.reset();

    // Hide error messages
    const registerError = document.getElementById('registerError');
    if (registerError) registerError.style.display = 'none';
}

function showRegisterForm(event) {
    if (event) event.preventDefault();

    document.getElementById('loginFormContainer').style.display = 'none';
    document.getElementById('passwordResetContainer').style.display = 'none';
    document.getElementById('registerFormContainer').style.display = 'block';
    document.getElementById('passwordResetSuccess').style.display = 'none';

    // Focus on email input
    setTimeout(() => {
        const emailInput = document.getElementById('id_register_email');
        if (emailInput) emailInput.focus();
    }, 100);
}

function submitRegistration(event) {
    event.preventDefault();

    const form = event.target;
    const formData = new FormData(form);
    const csrfToken = form.querySelector('[name=csrfmiddlewaretoken]').value;
    const errorDiv = document.getElementById('registerError');

    // Client-side validation
    const password1 = formData.get('password1');
    const password2 = formData.get('password2');

    if (password1 !== password2) {
        errorDiv.textContent = 'Пароли не совпадают';
        errorDiv.style.display = 'block';
        return;
    }

    // Hide previous errors
    errorDiv.style.display = 'none';

    // Send registration request
    fetch('/users/api/register/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken
        },
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Registration successful - reload page to show logged in state
            window.location.reload();
        } else {
            // Show error message
            errorDiv.textContent = data.error || 'Ошибка при регистрации';
            errorDiv.style.display = 'block';
        }
    })
    .catch(error => {
        console.error('Error:', error);
        errorDiv.textContent = 'Ошибка при регистрации';
        errorDiv.style.display = 'block';
    });
}

function submitPasswordReset(event) {
    event.preventDefault();

    const form = event.target;
    const formData = new FormData(form);
    const csrfToken = form.querySelector('[name=csrfmiddlewaretoken]').value;

    // Send password reset request
    fetch(form.action || '{% url "users:password_reset" %}', {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken
        },
        body: formData
    })
    .then(response => {
        if (response.ok) {
            // Show success message
            document.getElementById('passwordResetContainer').style.display = 'none';
            document.getElementById('passwordResetSuccess').style.display = 'block';
        } else {
            showToast('Ошибка при отправке запроса', 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showToast('Ошибка при отправке запроса', 'error');
    });
}

// Close modal on Escape key
document.addEventListener('keydown', function(event) {
    if (event.key === 'Escape') {
        closeLoginModal();
        closeSearchOverlay();
    }
});

// ============================================
// Search Overlay (VC.ru Style)
// ============================================
function openSearchOverlay() {
    const overlay = document.getElementById('searchOverlay');
    const input = document.getElementById('searchOverlayInput');

    if (overlay) {
        overlay.style.display = 'block';
        document.body.style.overflow = 'hidden';

        // Focus on input after animation
        setTimeout(() => {
            if (input) input.focus();
        }, 100);
    }
}

function closeSearchOverlay(event) {
    const overlay = document.getElementById('searchOverlay');

    if (overlay && (!event || event.target === overlay || event.target.classList.contains('search-overlay-close'))) {
        overlay.style.display = 'none';
        document.body.style.overflow = '';

        // Clear search input and results
        const input = document.getElementById('searchOverlayInput');
        const results = document.getElementById('searchResults');

        if (input) input.value = '';
        if (results) {
            results.style.display = 'none';
            results.innerHTML = '';
        }
    }
}

// Search functionality with debounce
let searchDebounceTimer;

function handleSearchInput() {
    const input = document.getElementById('searchOverlayInput');
    if (!input) return;

    clearTimeout(searchDebounceTimer);

    searchDebounceTimer = setTimeout(() => {
        const query = input.value.trim();
        if (query.length >= 2) {
            performSearch(query);
        } else {
            hideSearchResults();
        }
    }, 300);
}

function performSearch(query) {
    const results = document.getElementById('searchResults');
    if (!results) return;

    // Show loading state
    results.style.display = 'block';
    results.innerHTML = '<div class="search-loading">Поиск...</div>';

    // Fetch search results
    fetch(`/api/search/?q=${encodeURIComponent(query)}`)
        .then(response => response.json())
        .then(data => {
            displaySearchResults(data.results);
        })
        .catch(error => {
            console.error('Search error:', error);
            results.innerHTML = '<div class="search-error">Ошибка при поиске</div>';
        });
}

function displaySearchResults(results) {
    const container = document.getElementById('searchResults');
    if (!container) return;

    if (results.length === 0) {
        container.innerHTML = '<div class="search-no-results">Ничего не найдено</div>';
        return;
    }

    let html = '<div class="search-results-list">';
    html += '<h3 class="search-section-title">Результаты поиска</h3>';

    results.forEach(result => {
        html += `
            <a href="${result.url}" class="search-result-item">
                <div class="search-result-title">${result.title}</div>
                ${result.excerpt ? `<div class="search-result-excerpt">${result.excerpt}</div>` : ''}
            </a>
        `;
    });

    html += '</div>';
    container.innerHTML = html;
}

function hideSearchResults() {
    const results = document.getElementById('searchResults');
    if (results) {
        results.style.display = 'none';
        results.innerHTML = '';
    }
}

// ============================================
// User Dropdown Menu (Updated for Minimal Design)
// ============================================
function toggleUserDropdown() {
    const dropdown = document.getElementById('userDropdown');
    if (dropdown) {
        dropdown.classList.toggle('active');
    }
}

// Close dropdown when clicking outside
document.addEventListener('click', function(event) {
    const userMenu = document.querySelector('.user-menu-minimal');
    const dropdown = document.getElementById('userDropdown');

    if (dropdown && userMenu && !userMenu.contains(event.target)) {
        dropdown.classList.remove('active');
    }
});

// ============================================
// Mobile Menu
// ============================================
function toggleMobileMenu() {
    const navMenu = document.querySelector('.nav-menu');
    const mobileBtn = document.querySelector('.mobile-menu-btn');

    if (navMenu && mobileBtn) {
        navMenu.classList.toggle('active');
        mobileBtn.classList.toggle('active');
    }
}

// ============================================
// Auto-hide Messages
// ============================================
function initMessages() {
    const alerts = document.querySelectorAll('.alert');

    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.animation = 'slideOut 0.3s ease-out';
            setTimeout(() => {
                alert.remove();
            }, 300);
        }, 5000);
    });
}

// ============================================
// Smooth Scroll
// ============================================
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// ============================================
// Reading Progress Bar
// ============================================
function initReadingProgress() {
    const progressBar = document.querySelector('.reading-progress');
    if (!progressBar) return;

    window.addEventListener('scroll', () => {
        const winScroll = document.body.scrollTop || document.documentElement.scrollTop;
        const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
        const scrolled = (winScroll / height) * 100;

        progressBar.style.width = scrolled + '%';
    });
}

// ============================================
// Image Lazy Loading
// ============================================
function initLazyLoading() {
    const images = document.querySelectorAll('img[data-src]');

    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.removeAttribute('data-src');
                observer.unobserve(img);
            }
        });
    });

    images.forEach(img => imageObserver.observe(img));
}

// ============================================
// Like/Bookmark Functionality
// ============================================
function toggleReaction(articleId, reactionType) {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;

    fetch(`/articles/${articleId}/reaction/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({
            reaction_type: reactionType
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            updateReactionButton(articleId, reactionType, data.active);
            updateReactionCount(articleId, reactionType, data.count);
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function updateReactionButton(articleId, reactionType, active) {
    const button = document.querySelector(`[data-article-id="${articleId}"][data-reaction="${reactionType}"]`);
    if (button) {
        button.classList.toggle('active', active);
    }
}

function updateReactionCount(articleId, reactionType, count) {
    const countElement = document.querySelector(`[data-article-id="${articleId}"][data-reaction-count="${reactionType}"]`);
    if (countElement) {
        countElement.textContent = count;
    }
}

// ============================================
// Form Validation
// ============================================
function validateForm(formId) {
    const form = document.getElementById(formId);
    if (!form) return false;

    const requiredFields = form.querySelectorAll('[required]');
    let isValid = true;

    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            field.classList.add('error');
            isValid = false;
        } else {
            field.classList.remove('error');
        }
    });

    return isValid;
}

// ============================================
// Character Counter
// ============================================
function initCharCounter(textareaId, counterId, maxLength) {
    const textarea = document.getElementById(textareaId);
    const counter = document.getElementById(counterId);

    if (!textarea || !counter) return;

    textarea.addEventListener('input', () => {
        const currentLength = textarea.value.length;
        counter.textContent = `${currentLength}/${maxLength}`;

        if (currentLength > maxLength) {
            counter.classList.add('error');
        } else {
            counter.classList.remove('error');
        }
    });
}

// ============================================
// Search Autocomplete
// ============================================
function initSearchAutocomplete() {
    const searchInput = document.querySelector('.search-input');
    if (!searchInput) return;

    let debounceTimer;

    searchInput.addEventListener('input', function() {
        clearTimeout(debounceTimer);

        debounceTimer = setTimeout(() => {
            const query = this.value.trim();
            if (query.length >= 2) {
                fetchSearchSuggestions(query);
            }
        }, 300);
    });
}

function fetchSearchSuggestions(query) {
    fetch(`/api/search/?q=${encodeURIComponent(query)}`)
        .then(response => response.json())
        .then(data => {
            displaySearchSuggestions(data.results);
        })
        .catch(error => {
            console.error('Search error:', error);
        });
}

function displaySearchSuggestions(results) {
    const container = document.querySelector('.search-suggestions');
    if (!container) return;

    container.innerHTML = '';

    results.forEach(result => {
        const item = document.createElement('a');
        item.href = result.url;
        item.className = 'search-suggestion-item';
        item.textContent = result.title;
        container.appendChild(item);
    });

    container.style.display = results.length > 0 ? 'block' : 'none';
}

// ============================================
// Copy to Clipboard
// ============================================
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showToast('Скопировано в буфер обмена');
    }).catch(err => {
        console.error('Failed to copy:', err);
    });
}

// ============================================
// Toast Notifications
// ============================================
function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `alert alert-${type}`;
    toast.textContent = message;

    const container = document.querySelector('.messages-container') || createMessagesContainer();
    container.appendChild(toast);

    setTimeout(() => {
        toast.style.animation = 'slideOut 0.3s ease-out';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

function createMessagesContainer() {
    const container = document.createElement('div');
    container.className = 'messages-container';
    document.body.appendChild(container);
    return container;
}

// ============================================
// Confirm Dialog
// ============================================
function confirmAction(message, callback) {
    if (confirm(message)) {
        callback();
    }
}

// ============================================
// VC.ru Style Independent Scrolling
// ============================================
function initIndependentScrolling() {
    const sidebarLeft = document.querySelector('.sidebar-left');
    const sidebarRight = document.querySelector('.sidebar-right');

    if (!sidebarLeft && !sidebarRight) return;

    // The CSS already handles the basic independent scrolling
    // with position: fixed and overflow-y: auto
    // The overscroll-behavior: contain prevents scroll chaining

    // Optional: Add smooth scrolling behavior
    if (sidebarLeft) {
        sidebarLeft.style.scrollBehavior = 'smooth';
    }

    if (sidebarRight) {
        sidebarRight.style.scrollBehavior = 'smooth';
    }
}

// ============================================
// Toggle All Categories
// ============================================
function toggleAllCategories() {
    const hiddenCategories = document.querySelectorAll('.category-hidden');
    const btn = document.getElementById('showAllCategoriesBtn');
    const icon = btn.querySelector('.show-all-icon');
    const text = btn.querySelector('.show-all-text');

    const isExpanded = btn.classList.contains('expanded');

    hiddenCategories.forEach(cat => {
        if (isExpanded) {
            cat.style.display = 'none';
        } else {
            cat.style.display = 'block';
        }
    });

    if (isExpanded) {
        btn.classList.remove('expanded');
        icon.textContent = '▼';
        text.textContent = 'Показать все';
    } else {
        btn.classList.add('expanded');
        icon.textContent = '▲';
        text.textContent = 'Скрыть';
    }
}

// ============================================
// Initialize on DOM Load
// ============================================
document.addEventListener('DOMContentLoaded', function() {
    // Initialize theme
    initTheme();

    // Initialize messages
    initMessages();

    // Initialize reading progress (if on article page)
    initReadingProgress();

    // Initialize lazy loading
    initLazyLoading();

    // Initialize search autocomplete
    initSearchAutocomplete();

    // Initialize independent scrolling for sidebars
    initIndependentScrolling();

    // Initialize search overlay input listener
    const searchOverlayInput = document.getElementById('searchOverlayInput');
    if (searchOverlayInput) {
        searchOverlayInput.addEventListener('input', handleSearchInput);
    }

    console.log('ArticleHub initialized');
});

// ============================================
// Service Worker Registration (for PWA)
// ============================================
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/sw.js')
            .then(registration => console.log('SW registered:', registration))
            .catch(error => console.log('SW registration failed:', error));
    });
}
