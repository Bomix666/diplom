const API_BASE_URL = 'http://localhost:8000/api';

// Функция для поиска городов
async function searchCities(query) {
    try {
        const response = await fetch(`${API_BASE_URL}/cities/search/?q=${encodeURIComponent(query)}`);
        if (!response.ok) throw new Error('Network response was not ok');
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error searching cities:', error);
        return [];
    }
}

// Функция для получения станций города
async function getStationsByCity(cityId) {
    try {
        const response = await fetch(`${API_BASE_URL}/stations/by_city/?city_id=${cityId}`);
        if (!response.ok) throw new Error('Network response was not ok');
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching stations:', error);
        return [];
    }
}

// Функция для поиска маршрутов
async function searchRoutes(departureCity, arrivalCity, date) {
    try {
        const response = await fetch(
            `${API_BASE_URL}/routes/search/?` + 
            `departure_city=${encodeURIComponent(departureCity)}&` +
            `arrival_city=${encodeURIComponent(arrivalCity)}&` +
            `date=${date}`
        );
        if (!response.ok) throw new Error('Network response was not ok');
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error searching routes:', error);
        throw error;
    }
}

// Функция для бронирования билета
async function bookTicket(routeId, seatNumber) {
    try {
        const response = await fetch(`${API_BASE_URL}/tickets/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                // Здесь должен быть токен авторизации
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            },
            body: JSON.stringify({
                route: routeId,
                seat_number: seatNumber
            })
        });
        if (!response.ok) throw new Error('Network response was not ok');
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error booking ticket:', error);
        throw error;
    }
}

// Функция для форматирования даты и времени
function formatDateTime(dateTimeStr) {
    const date = new Date(dateTimeStr);
    return date.toLocaleString('ru-RU', {
        day: '2-digit',
        month: 'long',
        hour: '2-digit',
        minute: '2-digit'
    });
}

// Функция для расчета длительности поездки
function calculateDuration(departure, arrival) {
    const start = new Date(departure);
    const end = new Date(arrival);
    const diff = end - start;
    const hours = Math.floor(diff / (1000 * 60 * 60));
    const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
    return `${hours} ч ${minutes} мин`;
} 