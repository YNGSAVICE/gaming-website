"""Weather Routes"""

from flask import Blueprint, request, jsonify
import requests
from datetime import datetime
import os

weather_bp = Blueprint('weather', __name__, url_prefix='/api/weather')

# OpenWeatherMap API configuration
OPENWEATHER_API_KEY = os.environ.get('OPENWEATHER_API_KEY', 'YOUR_API_KEY_HERE')
OPENWEATHER_BASE_URL = 'https://api.openweathermap.org/data/2.5'

@weather_bp.route('/current', methods=['GET'])
def get_current_weather():
    """Get current weather for a location."""
    city = request.args.get('city', 'New York')
    units = request.args.get('units', 'metric')  # metric, imperial, standard
    
    if not OPENWEATHER_API_KEY or OPENWEATHER_API_KEY == 'YOUR_API_KEY_HERE':
        return jsonify({'error': 'Weather API key not configured'}), 500
    
    try:
        url = f'{OPENWEATHER_BASE_URL}/weather'
        params = {
            'q': city,
            'appid': OPENWEATHER_API_KEY,
            'units': units
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        return jsonify({
            'city': data['name'],
            'country': data['sys']['country'],
            'temperature': data['main']['temp'],
            'feels_like': data['main']['feels_like'],
            'humidity': data['main']['humidity'],
            'pressure': data['main']['pressure'],
            'wind_speed': data['wind']['speed'],
            'wind_direction': data['wind'].get('deg', 0),
            'clouds': data['clouds']['all'],
            'description': data['weather'][0]['main'],
            'icon': data['weather'][0]['icon'],
            'visibility': data.get('visibility', 0),
            'sunrise': datetime.fromtimestamp(data['sys']['sunrise']).isoformat(),
            'sunset': datetime.fromtimestamp(data['sys']['sunset']).isoformat(),
            'timezone': data['timezone'],
            'units': units
        }), 200
    
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Failed to fetch weather: {str(e)}'}), 400

@weather_bp.route('/forecast', methods=['GET'])
def get_weather_forecast():
    """Get 5-day weather forecast for a location."""
    city = request.args.get('city', 'New York')
    units = request.args.get('units', 'metric')
    
    if not OPENWEATHER_API_KEY or OPENWEATHER_API_KEY == 'YOUR_API_KEY_HERE':
        return jsonify({'error': 'Weather API key not configured'}), 500
    
    try:
        url = f'{OPENWEATHER_BASE_URL}/forecast'
        params = {
            'q': city,
            'appid': OPENWEATHER_API_KEY,
            'units': units
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        forecast_list = []
        for item in data['list']:
            forecast_list.append({
                'datetime': item['dt_txt'],
                'temperature': item['main']['temp'],
                'feels_like': item['main']['feels_like'],
                'humidity': item['main']['humidity'],
                'pressure': item['main']['pressure'],
                'wind_speed': item['wind']['speed'],
                'description': item['weather'][0]['main'],
                'icon': item['weather'][0]['icon'],
                'clouds': item['clouds']['all']
            })
        
        return jsonify({
            'city': data['city']['name'],
            'country': data['city']['country'],
            'forecast': forecast_list,
            'units': units
        }), 200
    
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Failed to fetch forecast: {str(e)}'}), 400

@weather_bp.route('/geo-weather', methods=['GET'])
def get_geo_weather():
    """Get weather by latitude and longitude."""
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    units = request.args.get('units', 'metric')
    
    if not lat or not lon:
        return jsonify({'error': 'Latitude and longitude required'}), 400
    
    if not OPENWEATHER_API_KEY or OPENWEATHER_API_KEY == 'YOUR_API_KEY_HERE':
        return jsonify({'error': 'Weather API key not configured'}), 500
    
    try:
        url = f'{OPENWEATHER_BASE_URL}/weather'
        params = {
            'lat': lat,
            'lon': lon,
            'appid': OPENWEATHER_API_KEY,
            'units': units
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        return jsonify({
            'city': data['name'],
            'country': data['sys']['country'],
            'latitude': data['coord']['lat'],
            'longitude': data['coord']['lon'],
            'temperature': data['main']['temp'],
            'feels_like': data['main']['feels_like'],
            'humidity': data['main']['humidity'],
            'pressure': data['main']['pressure'],
            'wind_speed': data['wind']['speed'],
            'wind_direction': data['wind'].get('deg', 0),
            'clouds': data['clouds']['all'],
            'description': data['weather'][0]['main'],
            'icon': data['weather'][0]['icon'],
            'visibility': data.get('visibility', 0),
            'units': units
        }), 200
    
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Failed to fetch weather: {str(e)}'}), 400

@weather_bp.route('/search', methods=['GET'])
def search_cities():
    """Search for cities."""
    query = request.args.get('q')
    limit = request.args.get('limit', 10, type=int)
    
    if not query:
        return jsonify({'error': 'Search query required'}), 400
    
    if not OPENWEATHER_API_KEY or OPENWEATHER_API_KEY == 'YOUR_API_KEY_HERE':
        return jsonify({'error': 'Weather API key not configured'}), 500
    
    try:
        url = f'{OPENWEATHER_BASE_URL}/find'
        params = {
            'q': query,
            'type': 'like',
            'appid': OPENWEATHER_API_KEY,
            'cnt': limit
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        cities = []
        for item in data.get('list', []):
            cities.append({
                'name': item['name'],
                'country': item['sys']['country'],
                'latitude': item['coord']['lat'],
                'longitude': item['coord']['lon'],
                'temperature': item['main']['temp']
            })
        
        return jsonify(cities), 200
    
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Search failed: {str(e)}'}), 400
