from flask import Blueprint, request, jsonify
import logging
from bson.objectid import ObjectId
import json
from bson import json_util
from db_init import mongo  # Import the mongo object from db_init.py

turtle_api = Blueprint('turtle_api', __name__)

@turtle_api.route('/add_turtle', methods=['POST'])
def add_turtle():
    try:
        turtle_data = request.json
        if not turtle_data:
            logging.error('Missing data for adding turtle')
            return jsonify({'error': 'Missing data'}), 400
        mongo.db.turtles.insert_one(turtle_data)
        logging.info('Turtle added successfully')
        return jsonify({'message': 'Turtle added successfully'}), 201
    except Exception as e:
        logging.exception('Failed to add turtle: %s', str(e))
        return jsonify({'error': 'Failed to add turtle'}), 500

@turtle_api.route('/update_turtle/<turtle_id>', methods=['PUT'])
def update_turtle(turtle_id):
    try:
        turtle_data = request.json
        if not turtle_data:
            logging.error('Missing data for updating turtle')
            return jsonify({'error': 'Missing data'}), 400
        result = mongo.db.turtles.update_one({'_id': ObjectId(turtle_id)}, {'$set': turtle_data})
        if result.modified_count == 0:
            logging.info('Turtle not found for update')
            return jsonify({'error': 'Turtle not found'}), 404
        logging.info('Turtle updated successfully')
        return jsonify({'message': 'Turtle updated successfully'}), 200
    except Exception as e:
        logging.exception('Failed to update turtle: %s', str(e))
        return jsonify({'error': 'Failed to update turtle'}), 500

@turtle_api.route('/get_turtles', methods=['GET'])
def get_turtles():
    try:
        turtles = mongo.db.turtles.find()
        turtle_list = json.loads(json_util.dumps(turtles))
        logging.info('Retrieved turtles successfully')
        return jsonify(turtle_list), 200
    except Exception as e:
        logging.exception('Failed to retrieve turtles: %s', str(e))
        return jsonify({'error': 'Failed to retrieve turtles'}), 500