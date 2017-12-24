from config import  SERVER


class Location:
    def __init__(self, location, region=None, system=None, astro=None, region_int=None, system_int=None):
        try:
            self.short = location.split('loc=')[1]
        except (AttributeError, IndexError):
            self.short = str(location)

        if region_int:
            region = '0' + str(region_int) if region_int < 10 else str(region_int)
        if system_int:
            system = '0' + str(system_int) if system_int < 10 else str(system_int)

        if region:
            self.short += ":" + region
        if system:
            self.short += ":" + system
        if astro:
            self.short += ":" + astro


    def __str__(self):
        return self.short

    def __eq__(self, other):
        return self.short == other.short

    def __contains__(self, item):
        return self.short in item.short

    def __hash__(self):
        return hash(self.short)

    def region_int(self):
        return int(str(self.region())[-2:])

    def system_int(self):
        return int(str(self.system())[-2:])

    # FIXME: attribute?
    def full(self):
        return "{}/map.aspx?loc={}".format(SERVER, self.short)

    def galaxy(self):
        return Location("{}/map.aspx?loc={}".format(SERVER, self.short[:3]))

    def region(self):
        return Location("{}/map.aspx?loc={}".format(SERVER, self.short[:6]))

    def system(self):
        return Location("{}/map.aspx?loc={}".format(SERVER, self.short[:9]))

    def astro(self):
        return Location("{}/map.aspx?loc={}".format(SERVER, self.short[:12]))

    def is_galaxy(self):
        return len(self.short) == 3

    def is_region(self):
        return len(self.short) == 6

    def is_system(self):
        return len(self.short) == 9

    def is_astro(self):
        return len(self.short) == 12

    def distance(self, location):  # FIXME
        location_a = self.short[1:].replace(':','')
        location_b = str(location)[1:].replace(':','')

        dist_cluster = 2000*abs(int(location_a[0]) - int(location_b[0]))
        if dist_cluster:
            return dist_cluster

        dist_galaxy = 200*abs(int(location_a[1]) - int(location_b[1]))
        if dist_galaxy:
            return dist_galaxy

        ax = 10*int(location_a[2]) + int(location_a[4]) + int(location_a[6])/10.0
        ay = 10*int(location_a[3]) + int(location_a[5]) + int(location_a[7])/10.0
        bx = 10*int(location_b[2]) + int(location_b[4]) + int(location_b[6])/10.0
        by = 10*int(location_b[3]) + int(location_b[5]) + int(location_b[7])/10.0
        return round(0.9 + ((ax-bx)**2 + (ay-by)**2)**0.5)




if __name__ == "__main__":
    l = Location('http://jade.astroempires.com/map.aspx?loc=J05:69:55:10')
    print(l)
    print(l.galaxy())
    print(l.galaxy().short)
    print(l.galaxy().full())
    print(l.region())
    print(l.system())
    print(l.astro())
    assert Location('12345/map.aspx?loc=J05').is_galaxy()
    assert Location('12345/map.aspx?loc=J05:69').is_region()
    assert Location('12345/map.aspx?loc=J05:69:55').is_system()
    assert Location('12345/map.aspx?loc=J05:69:55:10').is_astro()
    assert Location('12345/map.aspx?loc=J05') == Location('12345/map.aspx?loc=J05')

    assert Location('12345/map.aspx?loc=J05') == Location('J05')

    assert l in l.galaxy()
    assert l in l.region()
    assert l in l.system()
    assert l in l.astro()
    assert Location('http://jade.astroempires.com/map.aspx?loc=J14:02:99') in \
           Location('http://jade.astroempires.com/map.aspx?loc=J14')

    d = {l: 'A'}
    assert d[l] == 'A'
    for k,v in d.items():
        print('{} {}'.format(k, v))

    assert Location('12345/map.aspx?loc=J05', '69', '55', '10') == Location('12345/map.aspx?loc=J05:69:55:10')

    print(Location('http://jade.astroempires.com/map.aspx?loc=J15:82:99:10').distance(
        Location('http://jade.astroempires.com/map.aspx?loc=J15:81:37:31')))
    print(Location('http://jade.astroempires.com/map.aspx?loc=J15:81:37:31').distance(
        Location('http://jade.astroempires.com/map.aspx?loc=J15:82:41:21')))
    print(Location('http://jade.astroempires.com/map.aspx?loc=J15:82:99:10').distance(
        Location('http://jade.astroempires.com/map.aspx?loc=J15:83:07:11')))

#    assert Location('J14:46:00:00').distance('J14:95:00:00') == 51
#    assert Location('J14:95:37:40').distance('J14:44:96:20') == 46
