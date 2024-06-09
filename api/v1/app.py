#!/usr/bin/python3
""" Flask Application """
from models import storage
from api.v1.views import app_views
from os import environ
from flask import Flask, render_template, make_response, jsonify
from flask_cors import CORS
from flasgger import Swagger
from flasgger.utils import swag_from

app_instance = Flask(__name__)
app_instance.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app_instance.register_blueprint(app_views)
cors_instance = CORS(app_instance, resources={r"/*": {"origins": "0.0.0.0"}})


@app_instance.teardown_appcontext
def close_storage(error):
    """ Close Storage """
    storage.close()


@app_instance.errorhandler(404)
def handle_not_found(error):
    """ Handle 404 Error
    ---
    responses:
      404:
        description: The requested resource was not found
    """
    return make_response(jsonify({'error': "Not found"}), 404)

app_instance.config['SWAGGER'] = {
    'title': 'AirBnB clone Restful API',
    'uiversion': 3
}

Swagger(app)


if __name__ == "__main__":
    """ Main Function """
    host_address = environ.get('HBNB_API_HOST')
    port_number = environ.get('HBNB_API_PORT')
    if not host_address:
        host_address = '0.0.0.0'
    if not port_number:
        port_number = '5000'
    app_instance.run(host=host_address, port=port_number, threaded=True)
