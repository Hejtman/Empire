# Empire
Python tools for [AE][1] game.

## buildup
Base build planning. Calculation of price vs performance.

## emperor
Does high level management of governors.
Decides how many + what kind of governors needed and when they do their work. 
Just time/priority serialisation. Emperor don't care about what or how they actually do.

### governors
Represents instantiation of certain plan or regular activity.
It is queue of small jobs which are started at certain time.
Job usually consists from checking an situation, performing re-action and 
according its result planning next job, time and priority.

#### occ
Regularly pillage given bases occupation list.

#### guard

#### probe

#### spy
Daily updating stats of players within visible regions.
Weakly updating stats of player within same galaxy.

### database

#### locations
Server is set in config.py (with account credentials and stuff which is not part of this repo).

```
Location is either galaxy, region, system or astro:
galaxy = http://jade.astroempires.com/map.aspx?loc=J05
region = http://jade.astroempires.com/map.aspx?loc=J05:69
system = http://jade.astroempires.com/map.aspx?loc=J05:69:55
astro  = http://jade.astroempires.com/map.aspx?loc=J05:69:55:10
```

Server
[1]: https://www.astroempires.com
