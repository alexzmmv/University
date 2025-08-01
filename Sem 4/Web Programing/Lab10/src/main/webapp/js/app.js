document.addEventListener('DOMContentLoaded', function() {
    
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        setupLoginValidation();
    }
    
    setupRouteSelection();
    
    setupConfirmationModals();
    
    setupAutoHideAlerts();
});

function setupLoginValidation() {
    const loginForm = document.getElementById('loginForm');
    const usernameInput = document.getElementById('username');
    const passwordInput = document.getElementById('password');
    const toggleLink = document.getElementById('toggleForm');
    const formTitle = document.getElementById('formTitle');
    const submitBtn = document.getElementById('submitBtn');
    const actionInput = document.getElementById('action');
    
    if (toggleLink) {
        toggleLink.addEventListener('click', function(e) {
            e.preventDefault();
            const isLogin = actionInput.value === 'login';
            
            if (isLogin) {
                actionInput.value = 'register';
                formTitle.textContent = 'Register';
                submitBtn.textContent = 'Register';
                toggleLink.textContent = 'Already have an account? Login here';
            } else {
                actionInput.value = 'login';
                formTitle.textContent = 'Login';
                submitBtn.textContent = 'Login';
                toggleLink.textContent = 'Don\'t have an account? Register here';
            }
            
            usernameInput.value = '';
            passwordInput.value = '';
            clearValidationMessages();
        });
    }
    
    usernameInput.addEventListener('input', function() {
        validateUsername(this);
    });
    
    passwordInput.addEventListener('input', function() {
        validatePassword(this);
    });
    
    loginForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const isUsernameValid = validateUsername(usernameInput);
        const isPasswordValid = validatePassword(passwordInput);
        
        if (isUsernameValid && isPasswordValid) {
            this.submit();
        }
    });
}

function validateUsername(input) {
    const username = input.value.trim();
    const usernameRegex = /^[a-zA-Z0-9_]{3,20}$/;
    
    if (username === '') {
        showValidationMessage(input, 'Username is required', 'error');
        return false;
    } else if (!usernameRegex.test(username)) {
        showValidationMessage(input, 'Username must be 3-20 characters long and contain only letters, numbers, and underscores', 'error');
        return false;
    } else {
        showValidationMessage(input, 'Valid username', 'success');
        return true;
    }
}

function validatePassword(input) {
    const password = input.value;
    
    if (password === '') {
        showValidationMessage(input, 'Password is required', 'error');
        return false;
    } else if (password.length < 6) {
        showValidationMessage(input, 'Password must be at least 6 characters long', 'error');
        return false;
    } else {
        showValidationMessage(input, 'Valid password', 'success');
        return true;
    }
}

function showValidationMessage(input, message, type) {
    const existingMessage = input.parentNode.querySelector('.validation-message');
    if (existingMessage) {
        existingMessage.remove();
    }
    
    input.classList.remove('error', 'success');
    input.classList.add(type);
    
    const messageDiv = document.createElement('div');
    messageDiv.className = `validation-message ${type}`;
    messageDiv.textContent = message;
    input.parentNode.appendChild(messageDiv);
}

function clearValidationMessages() {
    const messages = document.querySelectorAll('.validation-message');
    messages.forEach(message => message.remove());
    
    const inputs = document.querySelectorAll('.form-control');
    inputs.forEach(input => {
        input.classList.remove('error', 'success');
    });
}

function setupRouteSelection() {
    const cityCards = document.querySelectorAll('.city-card');
    cityCards.forEach(card => {
        card.addEventListener('click', function() {
            const cityId = this.dataset.cityId;
            if (cityId) {
                selectCity(cityId);
            }
        });
    });
    
    const historyButtons = document.querySelectorAll('.back-to-btn');
    historyButtons.forEach(button => {
        button.addEventListener('click', function() {
            const index = this.dataset.index;
            const cityName = this.dataset.cityName;
            
            if (confirm(`Are you sure you want to go back to ${cityName}? This will remove all cities after it from your route.`)) {
                backToCity(index);
            }
        });
    });
}

function selectCity(cityId) {
    const form = document.createElement('form');
    form.method = 'POST';
    form.action = window.location.pathname;
    
    const actionInput = document.createElement('input');
    actionInput.type = 'hidden';
    actionInput.name = 'action';
    actionInput.value = 'selectCity';
    
    const cityInput = document.createElement('input');
    cityInput.type = 'hidden';
    cityInput.name = 'cityId';
    cityInput.value = cityId;
    
    form.appendChild(actionInput);
    form.appendChild(cityInput);
    document.body.appendChild(form);
    form.submit();
}

function backToCity(index) {
    const form = document.createElement('form');
    form.method = 'POST';
    form.action = window.location.pathname;
    
    const actionInput = document.createElement('input');
    actionInput.type = 'hidden';
    actionInput.name = 'action';
    actionInput.value = 'backTo';
    
    const indexInput = document.createElement('input');
    indexInput.type = 'hidden';
    indexInput.name = 'backToIndex';
    indexInput.value = index;
    
    form.appendChild(actionInput);
    form.appendChild(indexInput);
    document.body.appendChild(form);
    form.submit();
}

function setupConfirmationModals() {

    const clearRouteBtn = document.getElementById('clearRouteBtn');
    if (clearRouteBtn) {
        clearRouteBtn.addEventListener('click', function(e) {
            e.preventDefault();
            showConfirmationModal(
                'Clear Route',
                'Are you sure you want to clear your entire route? This action cannot be undone.',
                () => {
                    submitAction('clearRoute');
                }
            );
        });
    }
    
    const goBackBtn = document.getElementById('goBackBtn');
    if (goBackBtn) {
        goBackBtn.addEventListener('click', function(e) {
            e.preventDefault();
            submitAction('goBack');
        });
    }
    
    const newRouteBtn = document.getElementById('newRouteBtn');
    if (newRouteBtn) {
        newRouteBtn.addEventListener('click', function(e) {
            e.preventDefault();
            showConfirmationModal(
                'Start New Route',
                'Are you sure you want to start a new route? Your current route will be lost.',
                () => {
                    submitAction('newRoute');
                }
            );
        });
    }
    
    const logoutBtn = document.getElementById('logoutBtn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', function(e) {
            e.preventDefault();
            showConfirmationModal(
                'Logout',
                'Are you sure you want to logout? Your current route will be lost.',
                () => {
                    window.location.href = this.href;
                }
            );
        });
    }
}

function showConfirmationModal(title, message, onConfirm) {
    let modal = document.getElementById('confirmationModal');
    if (!modal) {
        modal = createConfirmationModal();
    }
    
    modal.querySelector('.modal-title').textContent = title;
    modal.querySelector('.modal-message').textContent = message;
    
    const confirmBtn = modal.querySelector('.confirm-btn');
    const cancelBtn = modal.querySelector('.cancel-btn');
    
    const newConfirmBtn = confirmBtn.cloneNode(true);
    confirmBtn.parentNode.replaceChild(newConfirmBtn, confirmBtn);
    
    newConfirmBtn.addEventListener('click', function() {
        modal.style.display = 'none';
        onConfirm();
    });
    
    cancelBtn.addEventListener('click', function() {
        modal.style.display = 'none';
    });
    
    modal.style.display = 'block';
    
    modal.addEventListener('click', function(e) {
        if (e.target === modal) {
            modal.style.display = 'none';
        }
    });
}

function createConfirmationModal() {
    const modal = document.createElement('div');
    modal.id = 'confirmationModal';
    modal.className = 'modal';
    
    modal.innerHTML = `
        <div class="modal-content">
            <h3 class="modal-title"></h3>
            <p class="modal-message"></p>
            <div class="modal-actions">
                <button type="button" class="btn btn-secondary cancel-btn">Cancel</button>
                <button type="button" class="btn btn-danger confirm-btn">Confirm</button>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    return modal;
}

function submitAction(action) {
    const form = document.createElement('form');
    form.method = 'POST';
    form.action = window.location.pathname;
    
    const actionInput = document.createElement('input');
    actionInput.type = 'hidden';
    actionInput.name = 'action';
    actionInput.value = action;
    
    form.appendChild(actionInput);
    document.body.appendChild(form);
    form.submit();
}

function setupAutoHideAlerts() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        const closeBtn = document.createElement('span');
        closeBtn.innerHTML = '&times;';
        closeBtn.style.cssText = 'float: right; cursor: pointer; font-size: 20px; font-weight: bold;';
        closeBtn.addEventListener('click', function() {
            alert.style.display = 'none';
        });
        alert.insertBefore(closeBtn, alert.firstChild);
        
        setTimeout(() => {
            if (alert.style.display !== 'none') {
                alert.style.opacity = '0';
                alert.style.transition = 'opacity 0.5s ease';
                setTimeout(() => {
                    alert.style.display = 'none';
                }, 500);
            }
        }, 5000);
    });
}

function showLoading(element) {
    const originalText = element.textContent;
    element.textContent = 'Loading...';
    element.disabled = true;
    
    return function hideLoading() {
        element.textContent = originalText;
        element.disabled = false;
    };
}

function makeRequest(url, method = 'GET', data = null) {
    return new Promise((resolve, reject) => {
        const xhr = new XMLHttpRequest();
        xhr.open(method, url);
        xhr.setRequestHeader('Content-Type', 'application/json');
        
        xhr.onload = function() {
            if (xhr.status >= 200 && xhr.status < 300) {
                try {
                    const response = JSON.parse(xhr.responseText);
                    resolve(response);
                } catch (e) {
                    resolve(xhr.responseText);
                }
            } else {
                reject(new Error(`Request failed with status ${xhr.status}`));
            }
        };
        
        xhr.onerror = function() {
            reject(new Error('Network error'));
        };
        
        xhr.send(data ? JSON.stringify(data) : null);
    });
}
