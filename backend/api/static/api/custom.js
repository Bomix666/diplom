// Анимация плавного появления карточек билетов
window.addEventListener('DOMContentLoaded', function() {
    const cards = document.querySelectorAll('.ticket-card');
    cards.forEach((card, i) => {
        setTimeout(() => {
            card.style.opacity = 1;
            card.style.transform = 'translateY(0)';
        }, 180 * i);
    });
    // Анимация появления блоков профиля
    document.querySelectorAll('.profile-card').forEach((el, i) => {
        setTimeout(() => {
            el.style.opacity = 1;
            el.style.transform = 'translateY(0)';
        }, 180 * i);
    });
    // Плавное переключение вкладок статистики
    const tabs = document.querySelectorAll('.profile-tab');
    const stats = document.querySelectorAll('.profile-stats-content');
    tabs.forEach((tab, idx) => {
        tab.addEventListener('click', function() {
            tabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');
            stats.forEach((s, i) => {
                s.style.display = (i === idx) ? 'block' : 'none';
            });
        });
    });
});

// Получение CSRF-токена
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
    return cookieValue;
}

// AJAX отмена билета с плавным исчезновением карточки
window.addEventListener('click', function(e) {
    if (e.target.classList.contains('btn-cancel')) {
        e.preventDefault();
        const ticketId = e.target.dataset.ticketId;
        const card = e.target.closest('.ticket-card');
        if (confirm('Вы уверены, что хотите отменить этот билет?')) {
            fetch(`/tickets/cancel/${ticketId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                }
            }).then(resp => {
                if (resp.ok) {
                    card.classList.add('removing');
                    setTimeout(() => card.remove(), 650);
                } else {
                    alert('Ошибка при отмене билета');
                }
            });
        }
    }
}); 