# Gaming Website

A full-featured gaming website built with Python, Flask, and modern web technologies.

## ✨ Features

- User authentication and profiles
- Multiple game types
- Real-time multiplayer support
- Leaderboards and scoring system
- User statistics and achievements
- **NEW:** 🕐 Digital Clock (multiple timezones)
- **NEW:** 🌤️ Weather Dashboard (OpenWeatherMap API)

## 📦 Project Structure

```
gaming-website/
├── backend/          # Flask backend
├── frontend/         # Web UI
├── database/         # Database schemas
├── tests/            # Test suite
├── docs/             # Documentation
├── DEPLOYMENT.md     # Deployment guides
└── RENDER_QUICKSTART.md  # Quick Render deployment guide
```

## 🛠 Tech Stack

- **Backend**: Flask
- **Frontend**: HTML5, CSS3, JavaScript
- **Database**: PostgreSQL / SQLite
- **Authentication**: JWT
- **Real-time**: WebSockets
- **Weather API**: OpenWeatherMap
- **Deployment**: Docker, Render, Railway, Heroku, AWS

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- pip
- PostgreSQL (or SQLite for development)
- Docker (optional, for containerized deployment)

### Local Development

```bash
# Clone the repository
git clone https://github.com/YNGSAVICE/gaming-website.git
cd gaming-website

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python backend/run.py
```

The application will be available at `http://localhost:5000`

### Using Docker (Development)

```bash
# Build and run with Docker Compose
docker-compose up

# Application will be at http://localhost:5000
```

## 📡 Deployment

### Quick Deploy to Render (Recommended)

See [RENDER_QUICKSTART.md](RENDER_QUICKSTART.md) for step-by-step instructions to deploy in 5 minutes.

**One-click deployment:**
1. Go to https://render.com
2. Connect your GitHub account
3. Select this repository
4. Deploy! ✅

### Other Deployment Options

For detailed deployment guides, see [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md):

- **Render** (Free tier available) - Recommended ⭐
- **Railway** (Easy setup, pay-as-you-go)
- **Heroku** (Classic choice, paid)
- **AWS EC2** (Most scalable)
- **DigitalOcean** (Affordable VPS)

### Production Deployment

```bash
# Using production docker-compose
docker-compose -f docker-compose.prod.yml up

# Environment variables needed
export FLASK_ENV=production
export SECRET_KEY=your-secret-key
export JWT_SECRET_KEY=your-jwt-secret
export DATABASE_URL=postgresql://user:password@host/dbname
export OPENWEATHER_API_KEY=your-api-key
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
FLASK_ENV=development
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret
DATABASE_URL=sqlite:///gaming.db
OPENWEATHER_API_KEY=your-openweather-api-key
```

For production, use `.env.production` (see `.env.production.example`).

## 📚 Features Overview

### Digital Clock 🕐
- Real-time clock with multiple timezone support
- Analog and digital display
- Add/remove favorite timezones
- 12/24 hour format toggle
- Live updating with smooth animations

**Access:** `http://localhost:5000/frontend/clock/index.html`

### Weather Dashboard 🌤️
- Real-time weather data from OpenWeatherMap API
- Current conditions and 5-day forecast
- Search for cities with autocomplete
- Track multiple favorite cities
- Metric/Imperial units toggle
- Beautiful glassmorphism UI design

**Access:** `http://localhost:5000/frontend/weather/index.html`

## 🧪 Testing

```bash
# Run tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=backend
```

## 📖 Development

See [CONTRIBUTING.md](CONTRIBUTING.md) for development guidelines.

### Running in Development Mode

```bash
# Enable debug mode
export FLASK_ENV=development

# Run with auto-reload
python backend/run.py
```

## 🐳 Docker Commands

```bash
# Development
docker-compose up

# Production
docker-compose -f docker-compose.prod.yml up -d

# View logs
docker-compose logs -f web

# Stop services
docker-compose down
```

## 🔐 Security

- JWT authentication for API endpoints
- CORS protection
- Rate limiting (in production)
- Security headers configured
- Password hashing with bcrypt
- Environment variable management

## 📊 Monitoring

In production, monitor your application:

- **Render Dashboard**: https://dashboard.render.com
- **Logs**: Check service logs in dashboard
- **Health Check**: `/health` endpoint
- **Metrics**: CPU, memory, requests per minute

## 🐛 Troubleshooting

### "Port 5000 already in use"
```bash
lsof -ti:5000 | xargs kill -9
```

### "Database connection failed"
- Ensure PostgreSQL is running
- Check DATABASE_URL format
- Verify credentials

### "Module not found"
```bash
pip install -r requirements.txt
```

### "API key errors"
- Get OpenWeatherMap API key: https://openweathermap.org/api
- Add to `.env` file as `OPENWEATHER_API_KEY`

## 📝 API Documentation

### Clock API

```
GET /api/clock/time?tz=UTC&format24=false
GET /api/clock/multi?tz=UTC&tz=US/Eastern&format24=false
GET /api/clock/timezones
```

### Weather API

```
GET /api/weather/current?city=London&units=metric
GET /api/weather/forecast?city=London&units=metric
GET /api/weather/geo-weather?lat=51.5074&lon=-0.1278
GET /api/weather/search?q=London&limit=10
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

## 🚀 Next Steps

- [ ] Deploy to Render (see [RENDER_QUICKSTART.md](RENDER_QUICKSTART.md))
- [ ] Add custom domain
- [ ] Set up monitoring and alerts
- [ ] Configure SSL/HTTPS
- [ ] Add analytics tracking
- [ ] Implement caching (Redis)
- [ ] Add database backups

## 📞 Support & Resources

- **Deployment Guide**: [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)
- **Render Quick Start**: [RENDER_QUICKSTART.md](RENDER_QUICKSTART.md)
- **Render Docs**: https://render.com/docs
- **Flask Docs**: https://flask.palletsprojects.com
- **OpenWeatherMap**: https://openweathermap.org/api

---

**Happy Gaming!** 🎮

For questions or issues, please open a GitHub issue or check the [documentation](docs/).
