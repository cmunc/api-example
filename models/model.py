from typing import List

import utils.log_utils as log


class DummyModel:
    """ A dummy model class serving as the interface to an actual, realistic ML model """

    def __init__(self) -> None:
        super().__init__()
        log.info("Recommendation model successfully initialized")

    def load(self, checkpoint: str, train_data_path: str) -> None:
        log.info(f"Recommendation model loaded with checkpoint '{checkpoint}' and data path '{train_data_path}'")

    def predict(self, user_id: int, n=5) -> List[str]:
        # Simulate two conditions:
        # - if ID is even, we've seen it before, and return personalized recommendations
        # - otherwise, it's a new user, we recommend the site-wide top movies
        if user_id % 2 == 0:
            return [f"personalized_movie{a}" for a in range(n)]
        else:
            return self.global_top_n(user_id)

    def global_top_n(self, user_id: int, n=5) -> List[str]:
        return [f"global_movie{a}" for a in range(n)]
