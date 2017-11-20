from config import  SERVER


class Location:
    def __init__(self, location):
        try:
            self.short = location.split('loc=')[1]
        except IndexError:
            self.short = location

    def __str__(self):
        return self.short

    def __eq__(self, other):
        return self.short == other.short

    def __contains__(self, item):
        return self.short in item.short

    def __hash__(self):
        return hash(self.short)

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
