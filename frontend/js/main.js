// API Base URL
const API_URL = 'http://localhost:5000/api';
let authToken = localStorage.getItem('authToken');
let currentUser = null;

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    if (authToken) {
        loadCurrentUser();
    }
    loadGames();
    loadLeaderboard();
});

// Authentication
async function handleLogin(event) {
    event.preventDefault();
    const form = event.target;
    const username = form.querySelector('input[type="text"]').value;
    const password = form.querySelector('input[type="password"]').value;

    try {
        const response = await fetch(`${API_URL}/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });

        if (response.ok) {
            const data = await response.json();
            authToken = data.access_token;
            currentUser = data.user;
            localStorage.setItem('authToken', authToken);
            closeModal();
            updateNav();
            loadLeaderboard();
        } else {
            alert('Login failed');
        }
    } catch (error) {
        console.error('Login error:', error);
        alert('An error occurred during login');
    }
}

async function loadCurrentUser() {
    try {
        const response = await fetch(`${API_URL}/users/me`, {
            headers: { 'Authorization': `Bearer ${authToken}` }
        });
        if (response.ok) {
            currentUser = await response.json();
            updateNav();
        }
    } catch (error) {
        console.error('Error loading user:', error);
    }
}

// Games
async function loadGames() {
    try {
        const response = await fetch(`${API_URL}/games`);
        const games = await response.json();
        const gamesList = document.getElementById('games-list');
        
        gamesList.innerHTML = games.map(game => `
            <div class="game-card">
                <div class="game-icon">🎮</div>
                <h3>${game.name}</h3>
                <p>${game.description || 'An awesome game'}</p>
                <button class="btn btn-primary" onclick="playGame(${game.id})">
                    Play Now
                </button>
            </div>
        `).join('');
    } catch (error) {
        console.error('Error loading games:', error);
    }
}

function playGame(gameId) {
    if (!authToken) {
        openModal();
    } else {
        alert(`Starting game ${gameId}...`);
    }
}

// Leaderboard
async function loadLeaderboard() {
    try {
        const response = await fetch(`${API_URL}/leaderboard/global?limit=10`);
        const leaderboard = await response.json();
        const leaderboardList = document.getElementById('leaderboard-list');
        
        if (leaderboard.length === 0) {
            leaderboardList.innerHTML = '<p>No scores yet. Be the first!</p>';
            return;
        }
        
        leaderboardList.innerHTML = `
            <table>
                <thead>
                    <tr>
                        <th>Rank</th>
                        <th>Player</th>
                        <th>Score</th>
                        <th>Games Played</th>
                    </tr>
                </thead>
                <tbody>
                    ${leaderboard.map(entry => `
                        <tr>
                            <td>${entry.rank}</td>
                            <td>${entry.display_name}</td>
                            <td>${entry.total_score}</td>
                            <td>${entry.games_played}</td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        `;
    } catch (error) {
        console.error('Error loading leaderboard:', error);
    }
}

// UI Helpers
function openModal() {
    document.getElementById('login-modal').style.display = 'block';
}

function closeModal() {
    document.getElementById('login-modal').style.display = 'none';
}

function updateNav() {
    if (currentUser) {
        document.querySelector('.login-link').style.display = 'none';
        document.querySelector('.profile-link').style.display = 'block';
    }
}

function scrollToSection(sectionId) {
    document.getElementById(sectionId).scrollIntoView({ behavior: 'smooth' });
}

function toggleAuthMode() {
    // Toggle between login and signup
    alert('Signup feature coming soon!');
}

// Close modal when clicking outside
window.onclick = function(event) {
    const modal = document.getElementById('login-modal');
    if (event.target == modal) {
        modal.style.display = 'none';
    }
}
