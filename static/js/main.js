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

