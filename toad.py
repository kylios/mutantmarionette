from marionette.units import Toad as MToad
from marionette.items import Grutonium
import math
import random

class Toad(MToad):
    
    def __init__(self):
        self.target = None
        self.num_items = 0

    def dist(self, pos1, pos2):
        return abs(math.sqrt((pos1[0] - pos2[0])**2 + \
                (pos1[1] - pos2[1])**2))

    def target_item(self, items):
        min_dist = -1
        target = None
        for item in items:
            dist = self.dist(self.pos, item.pos)
            if min_dist == -1 or dist < min_dist:
                target = item
                min_dist = dist
        return target

    def grab_item(self, item):
        self.grab(item.uid, item.amount)

    def move_towards_item(self, item):
        self.move(item.pos[0], item.pos[1])

    def act(self):

        # We can only perform one action per turn, so let's figure out what we 
        # want to do

        # Eat Grutonium if we have it
        if Grutonium in self.inventory and self.inventory[Grutonium]:
            self.eat(Grutonium, (self.max_health - self.health) / 2)
            return

        # Grab an item if we are on one
        if self.target and self.target.pos[0] == self.pos[0] and \
                self.target.pos[1] == self.pos[1]:
            if self.target.amount <= self.capacity - self.num_items:
                self.num_items = self.num_items + self.target.amount
                self.target = None
            else:
                self.num_items = self.capacity
            self.grab(self.target.uid, self.target.amount)
            return

        # items in view
        target = self.target_item(self.items_in_view)
        if target:
            if target.pos[0] == self.pos[0] and \
                target.pos[1] == self.pos[1]:
                self.grab_item(target)
            else:
                self.move_towards_item(target)
        else:
            self.move(random.randint(-1000, 1000), random.randint(-1000, 1000))


