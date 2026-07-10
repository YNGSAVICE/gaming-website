# Gaming Website

A full-featured gaming website built with Python, Flask, and modern web technologies.

## Features

- User authentication and profiles
- Multiple game types
- Real-time multiplayer support
- Leaderboards and scoring system
- User statistics and achievements

## Project Structure

```
gaming-website/
├── backend/          # Flask backend
├── frontend/         # Web UI
├── database/         # Database schemas
├── tests/            # Test suite
└── docs/             # Documentation
```

## Tech Stack

- **Backend**: Flask
- **Frontend**: HTML5, CSS3, JavaScript
- **Database**: PostgreSQL / SQLite
- **Authentication**: JWT
- **Real-time**: WebSockets

## Getting Started

### Prerequisites
- Python 3.8+
- pip
- PostgreSQL (or SQLite for development)

### Installation

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

## Development

See [CONTRIBUTING.md](CONTRIBUTING.md) for development guidelines.

## License

MIT License
