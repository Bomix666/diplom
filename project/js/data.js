// Моковые данные для станций и городов
const citiesAndStations = [
    {
        id: 1,
        name: "Москва",
        type: "city",
        stations: [
            { id: 1, name: "Киевский вокзал" },
            { id: 2, name: "Ленинградский вокзал" },
            { id: 3, name: "Казанский вокзал" }
        ]
    },
    {
        id: 2,
        name: "Санкт-Петербург",
        type: "city",
        stations: [
            { id: 4, name: "Московский вокзал" },
            { id: 5, name: "Ладожский вокзал" }
        ]
    },
    {
        id: 3,
        name: "Казань",
        type: "city",
        stations: [
            { id: 6, name: "Казань-1" },
            { id: 7, name: "Казань-2" }
        ]
    }
];

// Моковые данные для маршрутов
const routes = [
    {
        id: 1,
        from_city: "Москва",
        from_station: "Киевский вокзал",
        to_city: "Санкт-Петербург",
        to_station: "Московский вокзал",
        departure_time: "2024-04-20T10:00:00",
        arrival_time: "2024-04-20T18:00:00",
        price: 2500,
        available_seats: 15,
        bus_type: "Комфорт"
    },
    {
        id: 2,
        from_city: "Москва",
        from_station: "Казанский вокзал",
        to_city: "Казань",
        to_station: "Казань-1",
        departure_time: "2024-04-20T12:00:00",
        arrival_time: "2024-04-20T22:00:00",
        price: 3000,
        available_seats: 20,
        bus_type: "Стандарт"
    }
];

// Функция поиска городов и станций
function searchLocations(query) {
    if (!query) return [];
    query = query.toLowerCase();
    
    const results = [];
    citiesAndStations.forEach(city => {
        if (city.name.toLowerCase().includes(query)) {
            results.push({
                id: city.id,
                name: city.name,
                type: 'city'
            });
            
            city.stations.forEach(station => {
                results.push({
                    id: station.id,
                    name: `${station.name}, ${city.name}`,
                    type: 'station'
                });
            });
        }
    });
    
    return results;
}

// Функция поиска маршрутов
function searchRoutes(fromCity, toCity, date) {
    return routes.filter(route => {
        const routeDate = route.departure_time.split('T')[0];
        return route.from_city === fromCity && 
               route.to_city === toCity && 
               routeDate === date;
    });
}

// Функция форматирования даты и времени
function formatDateTime(dateTimeStr) {
    const date = new Date(dateTimeStr);
    return date.toLocaleString('ru-RU', {
        day: '2-digit',
        month: 'long',
        hour: '2-digit',
        minute: '2-digit'
    });
}

// Функция расчета длительности поездки
function calculateDuration(departure, arrival) {
    const start = new Date(departure);
    const end = new Date(arrival);
    const diff = end - start;
    const hours = Math.floor(diff / (1000 * 60 * 60));
    const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
    return `${hours} ч ${minutes} мин`;
} 