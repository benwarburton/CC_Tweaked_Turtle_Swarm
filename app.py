from flask import Flask, request, jsonify
import os
from config import DevelopmentConfig, ProductionConfig
from flask_pymongo import PyMongo
from custom_json_encoder import CustomJSONEncoder
from db_init import mongo, initialize_db  # Import the mongo object and initialize_db function from db_init.py

app = Flask(__name__)
app.json_encoder = CustomJSONEncoder

# Determine the configuration class based on the FLASK_ENV environment variable
config_class = DevelopmentConfig if os.environ.get('FLASK_ENV') == 'development' else ProductionConfig
app.config.from_object(config_class)

# Improved logging and error handling for MongoDB connection
try:
    # Configure MongoDB URI
    app.config["MONGO_URI"] = app.config.get("MONGODB_URI", "mongodb://localhost:27017/cc_tweaked_turtle_swarm")  # INPUT_REQUIRED {config_description: "Set your MongoDB URI here."}
    initialize_db(app)  # Initialize the database with the Flask app
    app.logger.info("MongoDB connected successfully.")
except Exception as e:
    app.logger.error("Failed to connect to MongoDB: %s", str(e), exc_info=True)

from api.turtle_api import turtle_api  # Import the turtle_api Blueprint after initializing the database
app.register_blueprint(turtle_api, url_prefix='/api')  # Register the turtle_api Blueprint

# Ensure routes are imported after the Flask app instance is created and configured
try:
    from routes import *  # Import all routes to ensure they are registered with the Flask app
    app.logger.info("Routes imported successfully.")
except Exception as e:
    app.logger.error("Failed to import routes: %s", str(e), exc_info=True)

if __name__ == '__main__':
    try:
        port = int(os.environ.get('PORT', 8080))  # Changed port to 8080 as per feedback
        app.logger.info(f'Starting the Flask application on port {port}')
        app.run(port=port)
    except Exception as e:
        app.logger.error('Failed to start the Flask application: %s\n%s', e, e.__traceback__)