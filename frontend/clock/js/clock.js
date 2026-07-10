const API_URL = 'http://localhost:5000/api';
let selectedTimezones = ['UTC', 'US/Eastern', 'Europe/London', 'Asia/Tokyo'];
let allTimezones = [];
let format24h = false;

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    loadTimezones();
    updateAllClocks();
    setInterval(updateAllClocks, 1000);
    
    document.getElementById('format24h').addEventListener('change', (e) => {
        format24h = e.target.checked;
        updateAllClocks();
    });
});

// Load available timezones
async function loadTimezones() {
    try {
        const response = await fetch(`${API_URL}/clock/timezones`);
        const data = await response.json();
        allTimezones = data.all;
    } catch (error) {
        console.error('Error loading timezones:', error);
    }
}

// Update all clock displays
async function updateAllClocks() {
    try {
        const tzParams = selectedTimezones.map(tz => `tz=${encodeURIComponent(tz)}`).join('&');
        const response = await fetch(`${API_URL}/clock/multi?${tzParams}&format24=${format24h}`);
        const clocks = await response.json();
        
        const grid = document.getElementById('clock-grid');
        grid.innerHTML = '';
        
        clocks.forEach((clock, index) => {
            const card = createClockCard(clock, index);
            grid.appendChild(card);
            updateAnalogClock(card, clock.datetime);
        });
    } catch (error) {
        console.error('Error updating clocks:', error);
    }
}

// Create clock card element
function createClockCard(clock, index) {
    const card = document.createElement('div');
    card.className = 'clock-card';
    card.id = `clock-${index}`;
    
    card.innerHTML = `
        <button class="clock-remove" onclick="removeTimezone('${clock.timezone}')">×</button>
        <div class="timezone-name">${clock.timezone}</div>
        <div class="analog-clock">
            <div class="hand hour-hand" id="hour-${index}"></div>
            <div class="hand minute-hand" id="minute-${index}"></div>
            <div class="hand second-hand" id="second-${index}"></div>
            <div class="clock-center"></div>
        </div>
        <div class="clock-time">${clock.time}</div>
        <div class="clock-date">${new Date(clock.datetime).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}</div>
        <div class="clock-day">${clock.day}</div>
        <div class="clock-offset">UTC ${clock.utc_offset.slice(0, 3)}:${clock.utc_offset.slice(3)}</div>
    `;
    
    return card;
}

// Update analog clock hands
function updateAnalogClock(card, datetime) {
    const date = new Date(datetime);
    const hours = date.getHours() % 12;
    const minutes = date.getMinutes();
    const seconds = date.getSeconds();
    
    const hourDeg = (hours * 30) + (minutes * 0.5);
    const minuteDeg = (minutes * 6) + (seconds * 0.1);
    const secondDeg = seconds * 6;
    
    const index = card.id.split('-')[1];
    document.getElementById(`hour-${index}`).style.transform = `rotate(${hourDeg}deg)`;
    document.getElementById(`minute-${index}`).style.transform = `rotate(${minuteDeg}deg)`;
    document.getElementById(`second-${index}`).style.transform = `rotate(${secondDeg}deg)`;
}

// Add timezone
function addTimezone() {
    const modal = document.getElementById('timezone-modal');
    const list = document.getElementById('timezone-list');
    
    list.innerHTML = allTimezones.map(tz => `
        <div class="timezone-item ${selectedTimezones.includes(tz) ? 'selected' : ''}" 
             onclick="selectTimezone('${tz}')">
            ${tz}
        </div>
    `).join('');
    
    modal.style.display = 'block';
}

// Select timezone
function selectTimezone(timezone) {
    if (selectedTimezones.includes(timezone)) {
        selectedTimezones = selectedTimezones.filter(tz => tz !== timezone);
    } else {
        selectedTimezones.push(timezone);
    }
    
    // Update UI
    document.querySelectorAll('.timezone-item').forEach(item => {
        if (item.textContent.trim() === timezone) {
            item.classList.toggle('selected');
        }
    });
    
    updateAllClocks();
}

// Remove timezone
function removeTimezone(timezone) {
    selectedTimezones = selectedTimezones.filter(tz => tz !== timezone);
    updateAllClocks();
}

// Search timezones
function searchTimezones() {
    const searchTerm = document.getElementById('timezone-search').value.toLowerCase();
    const items = document.querySelectorAll('.timezone-item');
    
    items.forEach(item => {
        if (item.textContent.toLowerCase().includes(searchTerm)) {
            item.style.display = 'block';
        } else {
            item.style.display = 'none';
        }
    });
}

// Close timezone modal
function closeTimezoneModal() {
    document.getElementById('timezone-modal').style.display = 'none';
}

// Close modal on outside click
window.onclick = function(event) {
    const modal = document.getElementById('timezone-modal');
    if (event.target == modal) {
        modal.style.display = 'none';
    }
}
