__all__ = ['base']


from Game.base.queue import Queue
from Game.base.structures import Structures
from Game.base.trade_routes import BaseTradeRoutes


class Base(Structures, BaseTradeRoutes):
    def __init__(self, area, solar, fertility, metal, gas, crystals, location,
                 basic_energy_production, basic_construction, fleet, technologies):
        BaseTradeRoutes.__init__(self)
        Structures.__init__(self)

        self.q_production = Queue(fleet)
        self.q_structures = Queue(self.structures)
        self.q_research = Queue(technologies)

        self.area = area
        self.solar = solar
        self.fertility = fertility
        self.metal = metal
        self.gas = gas
        self.crystals = crystals
        self.location = location
        self.basic_energy_production = basic_energy_production
        self.basic_construction = basic_construction
        self.technologies = technologies

    def get_eco(self):
        return self.structures['Metal Refineries'] + \
               self.structures['Crystal Mines'] * self.crystals + \
               self.structures['Robotic Factories'] + \
               self.structures['Shipyards'] + \
               self.structures['Orbital Shipyards'] * 2 + \
               self.structures['Spaceports'] * 2 + \
               self.structures['Nanite Factories'] * 2 + \
               self.structures['Android Factories'] * 2 + \
               self.structures['Economic Centers'] * 4 + \
               self.structures['Capital'] * 26

    def get_trade_income(self):
        self_income = sum(1.2 * min(self.get_eco(), b.eco)**0.5 for b in self.trade_routes_self)
        foreign_income = 1.2 * self.get_eco()**0.5 * self.trade_routes_foreign
        return self_income + foreign_income

    def free_routes_slots(self):
        spaceports = self.structures['Spaceports']
        routes_slots_used = len(self.trade_routes_self) + self.trade_routes_foreign
        routes_slots_max = (1 if spaceports else 0) + spaceports/5
        return routes_slots_max - routes_slots_used

    def get_area_available(self):
        return self.structures['Terraform'] * 5 + \
               self.structures['Multi-Level Platforms'] * 10

    def get_population_limit(self):
        return self.structures['Urban Structures']*self.fertility + \
               self.structures['Orbital Base']

    def get_energy_production(self):
        energy_structures_production = self.structures['Solar Plants'] * self.solar + \
                                       self.structures['Gas Plants'] * self.gas + \
                                       self.structures['Fusion Plants'] * 4 + \
                                       self.structures['Antimatter Plants'] * 10 + \
                                       self.structures['Orbital Plants'] * 12
        return (self.basic_energy_production + energy_structures_production) * (1 + 0.05*self.technologies['Energy'])

    def get_construction(self):
        construction = self.structures['Metal Refineries'] * self.metal + \
                       self.structures['Robotic Factories'] * 2 + \
                       self.structures['Nanite Factories'] * 4 + \
                       self.structures['Android Factories'] * 6
        return (self.basic_construction + construction) * (1 + 0.05*self.technologies['Cybernetics'])

    def get_production(self):
        production = self.structures['Metal Refineries'] * self.metal + \
                     self.structures['Robotic Factories'] * 2 + \
                     self.structures['Shipyards'] * 2 + \
                     self.structures['Orbital Shipyards'] * 8 + \
                     self.structures['Nanite Factories'] * 4 + \
                     self.structures['Android Factories'] * 6
        return production * (1 + 0.05*self.technologies['Cybernetics'])

    def get_research_resources(self):
        return 6*self.structures['Research Labs'] * (1 + 0.05*self.technologies['Artificial Intelligence'])


# UNIT TEST
if __name__ == "__main__":
    import json

    fl = None  # FIXME
    tech = None  # FIXME
    home = Base(85, 3, 5, 3, 1, 0, 'X14:54:16:41', 2, 40, fl, tech)
    expand = Base(85, 3, 5, 3, 1, 0, 'X14:55:16:41', 2, 20, fl, tech)

    print(json.dumps(home.__dict__, indent=4))
    # json.dumps(self, default=lambda o: o.__dict__, indent=4)
