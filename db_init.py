from flask_pymongo import PyMongo

mongo = PyMongo()

def initialize_db(app):
    try:
        mongo.init_app(app)
        app.logger.info("MongoDB initialized successfully.")
    except Exception as e:
        app.logger.error("Failed to initialize MongoDB: %s", str(e), exc_info=True)