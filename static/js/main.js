document.addEventListener('DOMContentLoaded', function() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            alert.style.transition = 'opacity 0.5s';
            alert.style.opacity = '0';
            setTimeout(function() {
                alert.remove();
            }, 500);
        }, 5000);
    });
});

function toggleUserMenu() {
    var dropdown = document.getElementById('userMenuDropdown');
    var button = document.querySelector('.user-menu-button');
    
    dropdown.classList.toggle('show');
    button.classList.toggle('active');
}

document.addEventListener('click', function(event) {
    var menu = document.querySelector('.user-menu');
    var dropdown = document.getElementById('userMenuDropdown');
    var button = document.querySelector('.user-menu-button');
    
    if (menu && !menu.contains(event.target)) {
        dropdown.classList.remove('show');
        button.classList.remove('active');
    }
});

function showTab(tabId, buttonElement) {
    var tabs = document.querySelectorAll('.tab-content');
    var buttons = document.querySelectorAll('.tab-button');
    
    tabs.forEach(function(tab) {
        tab.classList.remove('active');
    });
    
    buttons.forEach(function(btn) {
        btn.classList.remove('active');
    });
    
    document.getElementById(tabId).classList.add('active');
    if (buttonElement) {
        buttonElement.classList.add('active');
    }
}

document.addEventListener('DOMContentLoaded', function() {
    const dateInputs = document.querySelectorAll('input[type="date"]');
    const timeInputs = document.querySelectorAll('input[type="time"]');
    
    dateInputs.forEach(function(input) {
        input.addEventListener('click', function() {
            if (this.showPicker) {
                this.showPicker();
            }
        });
        input.addEventListener('focus', function() {
            if (this.showPicker) {
                this.showPicker();
            }
        });
    });
    
    timeInputs.forEach(function(input) {
        input.addEventListener('click', function() {
            if (this.showPicker) {
                this.showPicker();
            }
        });
        input.addEventListener('focus', function() {
            if (this.showPicker) {
                this.showPicker();
            }
        });
    });
});

function togglePasswordVisibility(inputId, button) {
    const input = document.getElementById(inputId);
    if (!input) return;
    
    const eyeIcon = button.querySelector('.eye-icon');
    if (!eyeIcon) return;
    
    if (input.type === 'password') {
        input.type = 'text';
        button.classList.add('active');
        eyeIcon.innerHTML = '<path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"></path><line x1="1" y1="1" x2="23" y2="23"></line>';
    } else {
        input.type = 'password';
        button.classList.remove('active');
        eyeIcon.innerHTML = '<path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path><circle cx="12" cy="12" r="3"></circle>';
    }
}

function toggleNotifications() {
    const dropdown = document.getElementById('notificationsDropdown');
    const button = document.getElementById('notificationsButton');
    
    if (!dropdown || !button) {
        console.error('Notification elements not found');
        return;
    }
    
    dropdown.classList.toggle('show');
    button.classList.toggle('active');
    
    if (dropdown.classList.contains('show')) {
        loadNotifications();
    }
}

function loadNotifications() {
    const list = document.getElementById('notificationsList');
    const badge = document.getElementById('notificationsBadge');
    
    if (!list || !badge) {
        return;
    }
    
    fetch('/notifications/')
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            if (!data) {
                throw new Error('Empty response');
            }
            
            badge.textContent = data.unread_count || 0;
            badge.style.display = (data.unread_count > 0) ? 'block' : 'none';
            
            if (!data.notifications || data.notifications.length === 0) {
                list.innerHTML = '<div class="notification-empty">Нет уведомлений</div>';
                return;
            }
            
            list.innerHTML = data.notifications.map(notif => {
                const appId = notif.application_id ? notif.application_id : 'null';
                return `
                <div class="notification-item ${notif.is_read ? 'read' : 'unread'}" onclick="markNotificationRead(${notif.id}, ${appId})">
                    <div class="notification-title">${escapeHtml(notif.title)}</div>
                    <div class="notification-message">${escapeHtml(notif.message)}</div>
                    <div class="notification-time">${escapeHtml(notif.created_at)}</div>
                </div>
            `;
            }).join('');
        })
        .catch(error => {
            console.error('Ошибка загрузки уведомлений:', error);
            if (list) {
                list.innerHTML = '<div class="notification-empty">Ошибка загрузки уведомлений</div>';
            }
        });
}

function markNotificationRead(notificationId, applicationId) {
    fetch(`/notifications/${notificationId}/read/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json',
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            loadNotifications();
            
            if (applicationId && applicationId !== 'null') {
                window.location.href = `/application/${applicationId}/`;
            }
        }
    })
    .catch(error => {
        console.error('Ошибка отметки уведомления:', error);
    });
}

function markAllNotificationsRead() {
    fetch('/notifications/read-all/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json',
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            loadNotifications();
        }
    })
    .catch(error => {
        console.error('Ошибка отметки всех уведомлений:', error);
    });
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    if (!cookieValue) {
        const metaTag = document.querySelector('meta[name="csrf-token"]');
        if (metaTag) {
            cookieValue = metaTag.getAttribute('content');
        }
    }
    return cookieValue;
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

document.addEventListener('click', function(event) {
    const container = document.querySelector('.notifications-container');
    const dropdown = document.getElementById('notificationsDropdown');
    const button = document.getElementById('notificationsButton');
    
    if (container && dropdown && button && !container.contains(event.target)) {
        dropdown.classList.remove('show');
        button.classList.remove('active');
    }
});

document.addEventListener('DOMContentLoaded', function() {
    if (document.getElementById('notificationsButton')) {
        loadNotifications();
        setInterval(loadNotifications, 30000);
    }
});

