from marionette.units import Toad as MToad
from marionette.items import Grutonium
import math
import random


class Toad(MToad):

    def __init__(self):
        self.direction = (0, 0)
        self.last_pos = (0, 0)
        self.target = None
        self.time = 0

        self.units = {}
        self.old_units = {}

    def dist(self, pos1, pos2):
        return math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)

    def dist_to_items(self, pos=None, possible_targets=None):
        if pos == None: pos = self.pos
        if possible_targets == None: possible_targets = self.items_in_view
        yield float('inf'), None
        for item in possible_targets:
            yield self.dist(pos, item.pos), item

    def calc_units(self):
        pass

    def calc_target(self):

#        while True:
#            dist, self.target = min(self.dist_to_items())
#            self.log_error("dist: %f, target: %s" % (dist, str(self.target)))
#
#            # List of objects to NOT target
#            bad_targets = []
#
#            for unit in self.units_in_view:
#
#                if unit.pos == self.pos:
#                    continue
#                
#                min_dist = 0
#                target = None
#                # Find the unit's nearest target
#                for t in self.items_in_view:
#                    d = math.sqrt((unit.pos[0] - t.pos[0])**2 + \
#                            (unit.pos[1] - t.pos[1])**2)
#                    if min_dist == 0 or d < min_dist:
#                        min_dist = d
#                        target = t
#                if self.target:
#                    if self.target.pos == target.pos and min_dist < dist:
#                        bad_targets.append(target)
#                else:
#                    bad_targets.append(target)
#
#            if self.target.pos not in (t.pos for t in bad_targets):
#                break
#

        bad_targets = []
        # Calculate all items targeted by other units and their distances to
        # those items
        for u in self.units_in_view:
            dist, target = min(self.dist_to_items(u.pos))
            if not target:
                continue
            my_dist = self.dist(self.pos, target.pos)

            if dist > my_dist:
                bad_targets.append(target)
            
        possible_targets = set(self.items_in_view) - set(bad_targets)
        self.target = min(self.dist_to_items(self.pos, possible_targets))[1]



    def calc_stuck(self):
        self.stuck = self.pos == self.last_pos

    def handle_eat(self):
        if (Grutonium in self.inventory and
            self.inventory[Grutonium] < self.max_health - self.health and
            self.inventory[Grutonium] > 0):
            self.eat(Grutonium, self.inventory[Grutonium])
            return True
        if Grutonium in self.inventory:
            self.log_error(self.inventory[Grutonium])
        return False

    def handle_die(self):
        roulette = random.randint(200)
        if roulette == 13:
            self.die()

    def handle_drop(self):
        roulette = random.randint(5)
        if roulette == 0 and Grutonium in self.inventory:
            self.drop(Grutonium, self.inventory[Grutonium])

    def handle_grab(self):
        if self.target and self.pos == self.target.pos:
            self.grab(self.target.uid, self.target.amount)
            return True
        return False

    def handle_move(self):
        if self.target:
            self.direction = self.target.pos
        elif self.stuck:
            x = random.randint(-1000, 1000)
            y = random.randint(-1000, 1000)
            self.direction = (self.pos[0] + x, self.pos[1] + y)
        self.move(*self.direction)
        return True

    def store_pos(self):
        self.last_pos = self.pos

    def act(self):
        calc = [
            self.calc_stuck,
            self.calc_units,
            self.calc_target,
        ]
        for c in calc:
            c()

        handle = [
            self.handle_eat,
            self.handle_grab,
            self.handle_move,
            #self.handle_drop,
            #self.handle_die,
        ]
        for h in handle:
            if h():
                break

        store = [
            self.store_pos,
        ]
        for s in store:
            s()

        self.time += 1
