"""Clock Routes"""

from flask import Blueprint, request, jsonify
from datetime import datetime
import pytz

clock_bp = Blueprint('clock', __name__, url_prefix='/api/clock')

# Common timezones
COMMON_TIMEZONES = {
    'UTC': 'UTC',
    'EST': 'US/Eastern',
    'CST': 'US/Central',
    'MST': 'US/Mountain',
    'PST': 'US/Pacific',
    'GMT': 'Europe/London',
    'CET': 'Europe/Paris',
    'IST': 'Asia/Kolkata',
    'JST': 'Asia/Tokyo',
    'AEST': 'Australia/Sydney',
    'NZST': 'Pacific/Auckland',
    'SGT': 'Asia/Singapore',
    'HKT': 'Asia/Hong_Kong',
    'BRT': 'America/Sao_Paulo',
    'SAST': 'Africa/Johannesburg',
}

@clock_bp.route('/time', methods=['GET'])
def get_current_time():
    """Get current time in specified timezone."""
    timezone = request.args.get('tz', 'UTC')
    format_24h = request.args.get('format24', 'false').lower() == 'true'
    
    try:
        tz = pytz.timezone(timezone)
        current_time = datetime.now(tz)
        
        time_format = '%H:%M:%S' if format_24h else '%I:%M:%S %p'
        
        return jsonify({
            'timezone': timezone,
            'time': current_time.strftime(time_format),
            'datetime': current_time.isoformat(),
            'day': current_time.strftime('%A'),
            'date': current_time.strftime('%B %d, %Y'),
            'utc_offset': str(current_time.strftime('%z'))
        }), 200
    except pytz.exceptions.UnknownTimeZoneError:
        return jsonify({'error': 'Unknown timezone'}), 400

@clock_bp.route('/timezones', methods=['GET'])
def get_timezones():
    """Get list of available timezones."""
    return jsonify({
        'common': COMMON_TIMEZONES,
        'all': pytz.all_timezones
    }), 200

@clock_bp.route('/multi', methods=['GET'])
def get_multi_timezone():
    """Get current time in multiple timezones."""
    timezones = request.args.getlist('tz')
    if not timezones:
        timezones = list(COMMON_TIMEZONES.values())
    
    format_24h = request.args.get('format24', 'false').lower() == 'true'
    
    try:
        result = []
        for tz_name in timezones:
            tz = pytz.timezone(tz_name)
            current_time = datetime.now(tz)
            time_format = '%H:%M:%S' if format_24h else '%I:%M:%S %p'
            
            result.append({
                'timezone': tz_name,
                'time': current_time.strftime(time_format),
                'datetime': current_time.isoformat(),
                'day': current_time.strftime('%A'),
                'utc_offset': str(current_time.strftime('%z'))
            })
        
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400
