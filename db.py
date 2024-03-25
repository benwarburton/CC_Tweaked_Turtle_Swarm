from flask_pymongo import PyMongo
from app import app

# Configure MongoDB URI
app.config["MONGO_URI"] = app.config.get("MONGODB_URI", "mongodb://localhost:27017/cc_tweaked_turtle_swarm")

# Initialize PyMongo with the Flask app
try:
    mongo = PyMongo(app)
    app.logger.info("MongoDB connected successfully.")
except Exception as e:
    app.logger.error("Failed to connect to MongoDB: %s", str(e), exc_info=True)