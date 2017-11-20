class Production:
    def __init__(self, eco, power, armor, shield, hangar, speed, shippiard, os):
        self.eco = eco
        self.power = power
        self.armor = armor
        self.shield = shield
        self.hangar = hangar
        self.speed = speed
        self.shippiard = shippiard
        self.orbital_shippiard = os
        self.prerequisites = None


PRODUCTION = {
    'Goods':         Production(eco=20,    power=0,   armor=0,   shield=0,  hangar=0,   speed=0,   shippiard=1,  os=0),
    'Fighters':      Production(eco=5,     power=2,   armor=2,   shield=0,  hangar=-1,  speed=0,   shippiard=1,  os=0),
    'Bombers':       Production(eco=10,	   power=4,   armor=2,   shield=0,  hangar=-1,  speed=0,   shippiard=2,  os=0),
    'Heavy Bombers': Production(eco=30,	   power=10,  armor=4,   shield=0,  hangar=-2,  speed=0,   shippiard=3,  os=0),
    'Ion Bombers':   Production(eco=60,	   power=12,  armor=4,   shield=1,  hangar=-2,  speed=0,   shippiard=3,  os=0),
    'Corvette':      Production(eco=20,	   power=4,   armor=4,   shield=0,  hangar=0,   speed=8,   shippiard=4,  os=0),
    'Recycler':      Production(eco=30,	   power=2,   armor=2,   shield=0,  hangar=0,   speed=5,   shippiard=5,  os=0),
    'Destroyer':     Production(eco=40,	   power=8,   armor=8,   shield=0,  hangar=0,   speed=5,   shippiard=6,  os=0),
    'Frigate':       Production(eco=80,	   power=12,  armor=12,  shield=0,  hangar=4,   speed=5,   shippiard=8,  os=0),
    'Ion Frigate':   Production(eco=120,   power=14,  armor=12,  shield=1,  hangar=4,   speed=5,   shippiard=8,  os=0),
    'Scout Ship':    Production(eco=40,	   power=1,   armor=2,   shield=0,  hangar=0,   speed=15,  shippiard=4,  os=0),
    'Outpost Ship':  Production(eco=100,   power=2,   armor=4,   shield=0,  hangar=0,   speed=3,   shippiard=8,  os=0),
    'Cruiser':       Production(eco=200,   power=24,  armor=24,  shield=2,  hangar=4,   speed=4,   shippiard=10, os=0),
    'Carrier':       Production(eco=400,   power=12,  armor=24,  shield=2,  hangar=60,  speed=4,   shippiard=12, os=0),
    'Heavy Cruiser': Production(eco=500,   power=48,  armor=48,  shield=4,  hangar=8,   speed=3,   shippiard=12, os=0),
    'Battleship':    Production(eco=2000,  power=168, armor=128, shield=10, hangar=40,  speed=3,   shippiard=16, os=0),
    'Fleet Carrier': Production(eco=2500,  power=64,  armor=96,  shield=8,  hangar=400, speed=3,   shippiard=16, os=0),
    'Dreadnought':   Production(eco=10000, power=756, armor=512, shield=20, hangar=200, speed=2.5, shippiard=20, os=1),
}

PRODUCTION['Fighters']     .prerequisites = lambda t: t['Laser'] >= 1
PRODUCTION['Bombers']      .prerequisites = lambda t: t['Missiles'] >= 1
PRODUCTION['Heavy Bombers'].prerequisites = lambda t: t['Plasma'] >= 14
PRODUCTION['Ion Bombers']  .prerequisites = lambda t: t['Ion'] >= 10 and t['Shielding'] >= 10
PRODUCTION['Corvette']     .prerequisites = lambda t: t['Laser'] >= 2 and stellar_armor(t, 1, 2)
PRODUCTION['Recycler']     .prerequisites = lambda t: t['Laser'] >= 1 and stellar_armor(t, 1, 2)
PRODUCTION['Destroyer']    .prerequisites = lambda t: t['Plasma'] >= 1 and stellar_armor(t, 2, 6)
PRODUCTION['Frigate']      .prerequisites = lambda t: t['Missiles'] >= 6 and stellar_armor(t, 4, 8)
PRODUCTION['Ion Frigate']  .prerequisites = lambda t: t['Ion'] >= 10 and stellar_armor(t, 4, 8) and t['Shielding'] >= 10
PRODUCTION['Scout Ship']   .prerequisites = lambda t: t['Warp Drive'] >= 1
PRODUCTION['Outpost Ship'] .prerequisites = lambda t: t['Warp Drive'] >= 1
PRODUCTION['Cruiser']      .prerequisites = lambda t: t['Plasma'] >= 4 and warp_armor_shield(t, 2, 10, 2)
PRODUCTION['Carrier']      .prerequisites = lambda t: t['Missiles'] >= 6 and warp_armor_shield(t, 4, 10, 2)
PRODUCTION['Heavy Cruiser'].prerequisites = lambda t: t['Plasma'] >= 6 and warp_armor_shield(t, 4, 12, 4)
PRODUCTION['Battleship']   .prerequisites = lambda t: t['Ion'] >= 6 and warp_armor_shield(t, 8, 16, 8)
PRODUCTION['Fleet Carrier'].prerequisites = lambda t: t['Ion'] >= 4 and warp_armor_shield(t, 8, 14, 6)
PRODUCTION['Dreadnought']  .prerequisites = lambda t: t['Photon'] >= 6 and warp_armor_shield(t, 12, 20, 10)


def stellar_armor(t, stellar, armor):
    return t['Stellar Drive'] >= stellar and t['Armor'] >= armor


def warp_armor_shield(t, warp, armor, shielding):
    return t['Warp Drive'] >= warp and t['Armor'] >= armor and t['Shielding'] >= shielding
