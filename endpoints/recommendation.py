from typing import Optional

from flask import make_response
from flask_restful import Resource

import utils.log_utils as log
from endpoints.api_wrappers import safe_request, log_response_time
from models.model import DummyModel


class RecommendEndpoint(Resource):
    path = "/recommend/<user_id>"
    recommender_model = DummyModel()

    @staticmethod
    def bind_self(api):
        api.add_resource(RecommendEndpoint, RecommendEndpoint.path)
        RecommendEndpoint.recommender_model.load("dummy_path", "dummy_data_path")

    @safe_request
    @log_response_time(endpoint_name="recommend")
    def get(self, user_id, uid):
        # Validate/clean user ID
        user_id = self.clean_user_id(user_id)
        if user_id is None:
            return make_response({"error": "Invalid user ID provided. User ID must be a number"}, 400)

        log.request(uid, f"Parsed user ID: {user_id}")
        predictions = self.recommender_model.predict(int(user_id))

        return make_response({"message": "OK", "recommendations": predictions}, 200)

    @staticmethod
    def clean_user_id(user_id: str) -> Optional[str]:
        """ Returns the cleaned UID if valid, otherwise returns None """
        # Assert that UID is a number
        if not user_id.isdigit():
            return None
        return str(user_id)
