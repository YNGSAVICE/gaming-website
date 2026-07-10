const API_URL = 'http://localhost:5000/api';
let userCities = ['London', 'Tokyo', 'New York', 'Sydney'];
let currentCity = 'London';
let units = 'metric';

// Weather icons mapping
const weatherIcons = {
    '01d': '☀️', '01n': '🌙',
    '02d': '⛅', '02n': '🌥️',
    '03d': '☁️', '03n': '☁️',
    '04d': '☁️', '04n': '☁️',
    '09d': '🌧️', '09n': '🌧️',
    '10d': '🌦️', '10n': '🌧️',
    '11d': '⛈️', '11n': '⛈️',
    '13d': '❄️', '13n': '❄️',
    '50d': '🌫️', '50n': '🌫️'
};

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    loadCurrentWeather(currentCity);
    loadForecast(currentCity);
    loadMultipleCities();
});

// Load current weather
async function loadCurrentWeather(city) {
    try {
        const response = await fetch(`${API_URL}/weather/current?city=${encodeURIComponent(city)}&units=${units}`);
        const data = await response.json();
        
        if (response.ok) {
            displayCurrentWeather(data);
            currentCity = city;
        } else {
            console.error('Error:', data.error);
        }
    } catch (error) {
        console.error('Error loading weather:', error);
    }
}

// Display current weather
function displayCurrentWeather(data) {
    const icon = weatherIcons[data.icon] || '🌤️';
    const tempUnit = units === 'metric' ? '°C' : '°F';
    const speedUnit = units === 'metric' ? 'm/s' : 'mph';
    
    const html = `
        <div class="weather-info">
            <div class="weather-main-info">
                <div class="weather-icon">${icon}</div>
                <div class="weather-details">
                    <div class="weather-city">${data.city}, ${data.country}</div>
                    <div class="weather-temp">${Math.round(data.temperature)}${tempUnit}</div>
                    <div class="weather-description">${data.description}</div>
                </div>
            </div>
            <div class="weather-stats">
                <div class="weather-stat">
                    <div class="stat-label">Feels Like</div>
                    <div class="stat-value">${Math.round(data.feels_like)}${tempUnit}</div>
                </div>
                <div class="weather-stat">
                    <div class="stat-label">Humidity</div>
                    <div class="stat-value">${data.humidity}%</div>
                </div>
                <div class="weather-stat">
                    <div class="stat-label">Wind Speed</div>
                    <div class="stat-value">${data.wind_speed} ${speedUnit}</div>
                </div>
                <div class="weather-stat">
                    <div class="stat-label">Pressure</div>
                    <div class="stat-value">${data.pressure} hPa</div>
                </div>
                <div class="weather-stat">
                    <div class="stat-label">Visibility</div>
                    <div class="stat-value">${(data.visibility / 1000).toFixed(1)} km</div>
                </div>
                <div class="weather-stat">
                    <div class="stat-label">Clouds</div>
                    <div class="stat-value">${data.clouds}%</div>
                </div>
            </div>
        </div>
    `;
    
    document.getElementById('current-weather').innerHTML = html;
}

// Load forecast
async function loadForecast(city) {
    try {
        const response = await fetch(`${API_URL}/weather/forecast?city=${encodeURIComponent(city)}&units=${units}`);
        const data = await response.json();
        
        if (response.ok) {
            displayForecast(data.forecast);
        }
    } catch (error) {
        console.error('Error loading forecast:', error);
    }
}

// Display forecast
function displayForecast(forecast) {
    const grid = document.getElementById('forecast-grid');
    grid.innerHTML = forecast.slice(0, 8).map(item => {
        const date = new Date(item.datetime);
        const icon = weatherIcons[item.icon] || '🌤️';
        const tempUnit = units === 'metric' ? '°C' : '°F';
        
        return `
            <div class="forecast-card">
                <div class="forecast-time">${date.toLocaleString('en-US', { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' })}</div>
                <div class="forecast-icon">${icon}</div>
                <div class="forecast-temp">${Math.round(item.temperature)}${tempUnit}</div>
                <div class="forecast-description">${item.description}</div>
                <div class="forecast-info">
                    💧 ${item.humidity}% | 💨 ${item.wind_speed} m/s
                </div>
            </div>
        `;
    }).join('');
}

// Load multiple cities
async function loadMultipleCities() {
    const grid = document.getElementById('cities-grid');
    grid.innerHTML = '';
    
    for (const city of userCities) {
        try {
            const response = await fetch(`${API_URL}/weather/current?city=${encodeURIComponent(city)}&units=${units}`);
            const data = await response.json();
            
            if (response.ok) {
                const icon = weatherIcons[data.icon] || '🌤️';
                const tempUnit = units === 'metric' ? '°C' : '°F';
                
                const card = document.createElement('div');
                card.className = 'city-card';
                card.innerHTML = `
                    <div class="city-card-header">
                        <div class="city-name">${data.city}</div>
                        <button class="remove-city" onclick="removeCity('${data.city}')">×</button>
                    </div>
                    <div class="city-icon">${icon}</div>
                    <div class="city-temp">${Math.round(data.temperature)}${tempUnit}</div>
                    <div class="city-weather">${data.description}</div>
                    <div class="city-stats">
                        <span>💧 ${data.humidity}%</span>
                        <span>💨 ${data.wind_speed} m/s</span>
                        <span>🧭 ${data.pressure} hPa</span>
                    </div>
                `;
                grid.appendChild(card);
            }
        } catch (error) {
            console.error(`Error loading weather for ${city}:`, error);
        }
    }
}

// Search weather
async function searchWeather() {
    const city = document.getElementById('city-search').value.trim();
    if (city) {
        loadCurrentWeather(city);
        loadForecast(city);
        document.getElementById('city-search').value = '';
        document.getElementById('search-suggestions').classList.remove('active');
    }
}

// Handle search keypress
function handleSearchKeypress(event) {
    if (event.key === 'Enter') {
        searchWeather();
    } else {
        searchCities(event.target.value);
    }
}

// Search cities with suggestions
async function searchCities(query) {
    if (!query || query.length < 2) {
        document.getElementById('search-suggestions').classList.remove('active');
        return;
    }
    
    try {
        const response = await fetch(`${API_URL}/weather/search?q=${encodeURIComponent(query)}&limit=5`);
        const cities = await response.json();
        
        if (response.ok && cities.length > 0) {
            const suggestions = document.getElementById('search-suggestions');
            suggestions.innerHTML = cities.map(city => `
                <div class="suggestion-item" onclick="selectCity('${city.name}')
                    title="${city.name}, ${city.country}">
                    <strong>${city.name}</strong>, ${city.country}
                    <br>
                    <small>${Math.round(city.temperature)}°C</small>
                </div>
            `).join('');
            suggestions.classList.add('active');
        }
    } catch (error) {
        console.error('Error searching cities:', error);
    }
}

// Select city from suggestions
function selectCity(city) {
    document.getElementById('city-search').value = city;
    searchWeather();
}

// Add city to favorites
function addCity() {
    const city = prompt('Enter city name:');
    if (city && !userCities.includes(city)) {
        userCities.push(city);
        loadMultipleCities();
    }
}

// Remove city from favorites
function removeCity(city) {
    userCities = userCities.filter(c => c !== city);
    loadMultipleCities();
}

// Toggle units
function toggleUnits() {
    units = units === 'metric' ? 'imperial' : 'metric';
    loadCurrentWeather(currentCity);
    loadForecast(currentCity);
    loadMultipleCities();
}
