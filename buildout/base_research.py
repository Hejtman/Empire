from utils import calculate_price, calculate_time
from research import RESEARCH


class BaseResearch:
    def __init__(self, base_structures):
        self.base_structures = base_structures
        self.researching_technology = None
        self.researching_finish_time = None

    def research_start(self, technology, game):
        research_cost = calculate_price(price=RESEARCH[technology].eco, level=game.technologies[technology])

        if technology not in [base.researching for base in game.bases] \
                and game.eco >= research_cost \
                and self.researching_finish_time is None \
                and self.base_structures['Research Labs'] >= RESEARCH[technology].lab_req:

            game.eco -= research_cost
            self.researching_technology = technology

            artificial_intelligence_level = game.technologies['Artificial Intelligence']
            research_resources = self.get_research_resources(artificial_intelligence_level)
            research_time = calculate_time(price=research_cost, resources=research_resources)
            self.researching_finish_time = game.time + research_time
            return True
        else:
            return False

    def research_finished(self, game_technologies):
        game_technologies[self.researching_technology] += 1
        self.researching_technology = None
        self.researching_finish_time = None

    def get_research_resources(self, artificial_intelligence_level):
        return 6 * self.base_structures['Research Labs'] * (1 + artificial_intelligence_level * 0.05)
