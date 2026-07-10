"""Application Entry Point"""

import os
from backend.app import create_app, socketio

if __name__ == '__main__':
    app = create_app(os.environ.get('FLASK_ENV', 'development'))
    
    # Run the Flask-SocketIO server
    socketio.run(
        app,
        host=os.environ.get('FLASK_HOST', '127.0.0.1'),
        port=int(os.environ.get('FLASK_PORT', 5000)),
        debug=os.environ.get('DEBUG', True)
    )
