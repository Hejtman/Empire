class Structures:
    def __init__(self):
        self.structures = {s: 0 for s in STRUCTURES.keys()}
        self.structures['Urban Structures'] = 1

    def get_area_occupied(self):
        return sum(self.structures[structure] * cost.area for structure, cost in STRUCTURES.items())

    def get_population_occupied(self):
        return sum(self.structures[structure]*cost.population for structure, cost in STRUCTURES.items())

    def get_energy_consumption(self):
        return sum(self.structures[structure] * cost.energy for structure, cost in STRUCTURES.items())


class Cost:
    def __init__(self, population, energy, area, eco):
        self.population = population
        self.energy = energy
        self.area = area
        self.eco = eco
        self.prerequisites = None


STRUCTURES = {
    'Urban Structures':       Cost(population=0, energy=0,  area=1, eco=1),
    'Solar Plants':           Cost(population=1, energy=0,  area=1, eco=1),
    'Gas Plants':             Cost(population=1, energy=0,  area=1, eco=1),
    'Fusion Plants':          Cost(population=1, energy=0,  area=1, eco=20),
    'Antimatter Plants':      Cost(population=1, energy=0,  area=1, eco=2000),
    'Orbital Plants':         Cost(population=1, energy=0,  area=0, eco=40000),
    'Research Labs':          Cost(population=1, energy=1,  area=1, eco=2),
    'Metal Refineries':       Cost(population=1, energy=1,  area=1, eco=1),
    'Crystal Mines':          Cost(population=1, energy=1,  area=1, eco=2),
    'Robotic Factories':      Cost(population=1, energy=1,  area=1, eco=5),
    'Shipyards':              Cost(population=1, energy=1,  area=1, eco=5),
    'Orbital Shipyards':      Cost(population=1, energy=12, area=0, eco=10000),
    'Spaceports':             Cost(population=1, energy=1,  area=1, eco=5),
    'Command Centers':        Cost(population=1, energy=1,  area=1, eco=20),
    'Nanite Factories':       Cost(population=1, energy=2,  area=1, eco=80),
    'Android Factories':      Cost(population=1, energy=4,  area=1, eco=1000),
    'Economic Centers':       Cost(population=1, energy=2,  area=1, eco=80),
    'Terraform':              Cost(population=0, energy=0,  area=0, eco=80),
    'Multi-Level Platforms':  Cost(population=0, energy=0,  area=0, eco=10000),
    'Orbital Base':           Cost(population=0, energy=0,  area=0, eco=2000),
    'Jump Gate':              Cost(population=1, energy=8,  area=0, eco=5000),
    'Biosphere Modification': Cost(population=1, energy=24, area=1, eco=20000),
    'Capital':                Cost(population=1, energy=12, area=1, eco=15000),
    'Missile Turrets':        Cost(population=1, energy=1,  area=1, eco=20),
    'Disruptor Turrets':      Cost(population=1, energy=8,  area=1, eco=4096),
    'Deflection Shields':     Cost(population=1, energy=8,  area=1, eco=4096),
    'Planetary Shields':      Cost(population=1, energy=16, area=1, eco=25000),
    'Planetary Ring':         Cost(population=1, energy=24, area=0, eco=50000)
}

STRUCTURES['Fusion Plants']         .prerequisites = lambda tech: tech['Energy'] >= 6
STRUCTURES['Antimatter Plants']     .prerequisites = lambda tech: tech['Energy'] >= 20
STRUCTURES['Orbital Plants']        .prerequisites = lambda tech: tech['Energy'] >= 25
STRUCTURES['Robotic Factories']     .prerequisites = lambda tech: tech['Computer'] >= 2
STRUCTURES['Orbital Shipyards']     .prerequisites = lambda tech: tech['Cybernetics'] >= 2
STRUCTURES['Nanite Factories']      .prerequisites = lambda tech: tech['Computer'] >= 10 and tech['Laser'] >= 8
STRUCTURES['Android Factories']     .prerequisites = lambda tech: tech['Artificial Intelligence '] >= 4
STRUCTURES['Economic Centers']      .prerequisites = lambda tech: tech['Computer'] >= 10
STRUCTURES['Terraform']             .prerequisites = lambda tech: tech['Computer'] >= 10 and tech['Energy'] >= 10
STRUCTURES['Multi-Level Platforms'] .prerequisites = lambda tech: tech['Armour'] >= 22
STRUCTURES['Orbital Base']          .prerequisites = lambda tech: tech['Computer'] >= 20
STRUCTURES['Jump Gate']             .prerequisites = lambda tech: tech['Warp Drive'] >= 12 and tech['Energy'] >= 20
STRUCTURES['Biosphere Modification'].prerequisites = lambda tech: tech['Computer'] >= 24 and tech['Energy'] >= 24
STRUCTURES['Capital']               .prerequisites = lambda tech: tech['Tachyon Communications'] >= 1
STRUCTURES['Missile Turrets']       .prerequisites = lambda tech: tech['Missiles'] >= 1
STRUCTURES['Disruptor Turrets']     .prerequisites = lambda tech: tech['Disruptor'] >= 1 and armor_shield(tech, 18, 8)
STRUCTURES['Deflection Shields']    .prerequisites = lambda tech: tech['Ion'] >= 6 and tech['Shielding'] >= 10
STRUCTURES['Planetary Shields']     .prerequisites = lambda tech: tech['Ion'] >= 10 and tech['Shielding'] >= 16
STRUCTURES['Planetary Ring']        .prerequisites = lambda tech: tech['Photon'] >= 10 and armor_shield(tech, 22, 12)


def armor_shield(tech, armor, shielding):
    return tech['Armour'] >= armor and tech['Shielding'] >= shielding
