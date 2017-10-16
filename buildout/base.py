from structures import STRUCTURES
from base_research import BaseResearch
from base_trade_routes import BaseTradeRoutes


class Base:
    def __init__(self, area, solar, fertility, metal, gas, crystals, location, energy, construction, game):

        self.solar = solar
        self.fertility = fertility
        self.metal = metal
        self.gas = gas
        self.crystals = crystals
        self.location = location

        self.population = 0
        self.population_limit = fertility
        self.energy = 0
        self.energy_limit = energy
        self.area = 1
        self.area_limit = area

        self.eco = 0
        self.construction = construction
        self.production = 0

        self.structures = {s: 0 for s in STRUCTURES.keys()}
        self.structures['Urban Structures'] = 1
        self.base_research = BaseResearch(self.structures)
        self.trade_routes = BaseTradeRoutes(self)

        self.game_technologies = game.technologies

    # FIXME: attributes
    def get_energy(self):
        return self.energy * (1 + self.game_technologies['Energy'] * 0.05)

    def get_construction(self):
        return self.construction * (1 + self.game_technologies['Cybernetics'] * 0.05)

    def get_production(self):
        return self.production * (1 + self.game_technologies['Cybernetics'] * 0.05)

    def increase(self, attribute, value):
        eval('{}.{} += {}'.format(self, attribute, value))
