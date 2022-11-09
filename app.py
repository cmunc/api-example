from flask import Flask, jsonify
from flask_restful import Api

import utils.log_utils as log
from endpoints import RecommendEndpoint


def create_app():
    app = Flask(__name__)
    api = Api(app)

    # Register endpoints
    RecommendEndpoint.bind_self(api)

    # Handle default error cases
    @app.errorhandler(404)
    def resource_not_found(e):
        return jsonify(error=str(e)), 404

    return app


if __name__ == "__main__":
    app = create_app()
    log.info("Starting example server...")
    app.run(host="0.0.0.0", port=5000)
