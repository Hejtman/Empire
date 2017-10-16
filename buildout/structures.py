class Structures:
    def __init__(self, population, energy, area, eco):
        self.population = population 
        self.energy = energy
        self.area = area
        self.eco = eco
        self.prerequisites = None
        self.benefits = None 


STRUCTURES = {
    'Urban Structures':       Structures(population=0, energy=0,  area=1, eco=1),
    'Solar Plants':           Structures(population=1, energy=0,  area=1, eco=1),
    'Gas Plants':             Structures(population=1, energy=0,  area=1, eco=1),
    'Fusion Plants':          Structures(population=1, energy=0,  area=1, eco=20),
    'Antimatter Plants':      Structures(population=1, energy=0,  area=1, eco=2000),
    'Orbital Plants':         Structures(population=1, energy=0,  area=0, eco=40000),
    'Research Labs':          Structures(population=1, energy=1,  area=1, eco=2),
    'Metal Refineries':       Structures(population=1, energy=1,  area=1, eco=1),
    'Crystal Mines':          Structures(population=1, energy=1,  area=1, eco=2),
    'Robotic Factories':      Structures(population=1, energy=1,  area=1, eco=5),
    'Shipyards':              Structures(population=1, energy=1,  area=1, eco=5),
    'Orbital Shipyards':      Structures(population=1, energy=12, area=0, eco=10000),
    'Spaceports':             Structures(population=1, energy=1,  area=1, eco=5),
    'Command Centers':        Structures(population=1, energy=1,  area=1, eco=20),
    'Nanite Factories':       Structures(population=1, energy=2,  area=1, eco=80),
    'Android Factories':      Structures(population=1, energy=4,  area=1, eco=1000),
    'Economic Centers':       Structures(population=1, energy=2,  area=1, eco=80),
    'Terraform':              Structures(population=0, energy=0,  area=0, eco=80),
    'Multi-Level Platforms':  Structures(population=0, energy=0,  area=0, eco=10000),
    'Orbital Base':           Structures(population=0, energy=0,  area=0, eco=2000),
    'Jump Gate':              Structures(population=1, energy=8,  area=0, eco=5000),
    'Biosphere Modification': Structures(population=1, energy=24, area=1, eco=20000),
    'Capital':                Structures(population=1, energy=12, area=1, eco=15000),
    'Missile Turrets':        Structures(population=1, energy=1,  area=1, eco=20),
    'Disruptor Turrets':      Structures(population=1, energy=8,  area=1, eco=4096),
    'Deflection Shields':     Structures(population=1, energy=8,  area=1, eco=4096),
    'Planetary Shields':      Structures(population=1, energy=16, area=1, eco=25000),
    'Planetary Ring':         Structures(population=1, energy=24, area=0, eco=50000)
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

STRUCTURES['Urban Structures']      .benefits = lambda b: b.increase('population_limit', b.fertility)
STRUCTURES['Solar Plants']          .benefits = lambda b: b.increase('energy_limit', b.solar),
STRUCTURES['Gas Plants']            .benefits = lambda b: b.increase('energy_limit', b.gas),
STRUCTURES['Fusion Plants']         .benefits = lambda b: b.increase('energy_limit', 4),
STRUCTURES['Antimatter Plants']     .benefits = lambda b: b.increase('energy_limit', 10),
STRUCTURES['Orbital Plants']        .benefits = lambda b: b.increase('energy_limit', 12),
STRUCTURES['Research Labs']         .benefits = lambda b: b.increase('research', 6),
STRUCTURES['Metal Refineries']      .benefits = lambda b: b.increase(1, b.metal, b.metal),
STRUCTURES['Crystal Mines']         .benefits = lambda b: b.increase('eco', 1),
STRUCTURES['Robotic Factories']     .benefits = lambda b: b.increase(1, 2, 2),
STRUCTURES['Shipyards']             .benefits = lambda b: b.increase('eco', 1) and b.increase('production', 2),
STRUCTURES['Orbital Shipyards']     .benefits = lambda b: b.increase('eco', 2) and b.increase('production', 8),
STRUCTURES['Spaceports']            .benefits = lambda b: b.increase('eco', 2),
STRUCTURES['Nanite Factories']      .benefits = lambda b: b.increase(2, 4, 4),
STRUCTURES['Android Factories']     .benefits = lambda b: b.increase(2, 6, 6),
STRUCTURES['Economic Centers']      .benefits = lambda b: b.increase('eco', 4),
STRUCTURES['Terraform']             .benefits = lambda b: b.increase('area_limit', 5),
STRUCTURES['Multi-Level Platforms'] .benefits = lambda b: b.increase('area_limit', 10),
STRUCTURES['Orbital Base']          .benefits = lambda b: b.increase('population_limit', 10),
STRUCTURES['Biosphere Modification'].benefits = lambda b: b.increase('fertility', 1),
STRUCTURES['Capital']               .benefits = lambda b: b.increase('economy', 26)  # 10capital + 8*2other bases


def increase(base, eco, construction, production):
    base.increase('eco', eco)
    base.increase('construction', construction)
    base.increase('production', production)


def armor_shield(tech, armor, shielding):
    return tech['Armour'] >= armor and tech['Shielding'] >= shielding
