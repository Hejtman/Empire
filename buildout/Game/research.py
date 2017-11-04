class Technology:
    def __init__(self, eco, lab_req, prerequisites=None):
        self.eco = eco
        self.lab_req = lab_req
        self.prerequisites = prerequisites


RESEARCH = {
    'Energy':                  Technology(eco=2,      lab_req=1),
    'Computer':                Technology(eco=2,      lab_req=1),
    'Armour':                  Technology(eco=4,      lab_req=2),
    'Laser':                   Technology(eco=4,      lab_req=2,  prerequisites=lambda tech: tech['Energy'] >= 2),
    'Missiles':                Technology(eco=8,      lab_req=4,  prerequisites=lambda tech: tech['Computer'] >= 4),
    'Stellar Drive':           Technology(eco=16,     lab_req=5,  prerequisites=lambda tech: tech['Energy'] >= 6),
    'Plasma':                  Technology(eco=32,     lab_req=6),
    'Warp Drive':              Technology(eco=64,     lab_req=8),
    'Shielding':               Technology(eco=128,    lab_req=10, prerequisites=lambda tech: tech['Energy'] >= 10),
    'Ion':                     Technology(eco=256,    lab_req=12),
    'Photon':                  Technology(eco=1024,   lab_req=16),
    'Artificial Intelligence': Technology(eco=2048,   lab_req=18, prerequisites=lambda tech: tech['Computer'] >= 20),
    'Disruptor':               Technology(eco=4096,   lab_req=20),
    'Cybernetics':             Technology(eco=8192,   lab_req=22),
    'Tachyon Communications':  Technology(eco=32768,  lab_req=24),
    'Anti-Gravity':            Technology(eco=100000, lab_req=26)
}

RESEARCH['Plasma']                 .prerequisites = lambda tech: tech['Energy'] >= 6 and tech['Laser'] >= 4
RESEARCH['Warp Drive']             .prerequisites = lambda tech: tech['Energy'] >= 8 and tech['Stellar Drive'] >= 4
RESEARCH['Ion']                    .prerequisites = lambda tech: tech['Energy'] >= 12 and tech['Laser'] >= 10
RESEARCH['Photon']                 .prerequisites = lambda tech: tech['Energy'] >= 16 and tech['Plasma'] >= 8
RESEARCH['Disruptor']              .prerequisites = lambda tech: tech['Energy'] >= 20 and tech['Laser'] >= 18
RESEARCH['Cybernetics']            .prerequisites = lambda tech: tech['Artificial Intelligence'] >= 6
RESEARCH['Tachyon Communications'] .prerequisites = lambda tech: tech['Energy'] >= 24 and tech['Computer'] >= 24
RESEARCH['Anti-Gravity']           .prerequisites = lambda tech: tech['Energy'] >= 26 and tech['Computer'] >= 26
