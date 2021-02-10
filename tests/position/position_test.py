#!/usr/bin/env python3

"""
Created on 10 Feb 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

Getting distance between two points based on latitude/longitude
https://stackoverflow.com/questions/19412462/getting-distance-between-two-points-based-on-latitude-longitude
"""

from scs_core.position.position import Position


# --------------------------------------------------------------------------------------------------------------------
# run...

p1 = Position(52.2296756, 21.0122287)
p2 = Position(52.2296756, 21.0122287)

print("distance (same point): %s" % p1.distance(p2))
print("-")

p1 = Position(52.2296756, 21.0122287)
p2 = Position(52.406374, 16.9251681)

print("distance: %s" % p1.distance(p2))
print("-")

p1 = Position(52.406374, 16.9251681)
p2 = Position(52.2296756, 21.0122287)

print("distance (reversed): %s" % p1.distance(p2))
print("-")

p1 = Position(52.2296756, 1.0122287)
p2 = Position(52.406374, -3.0748319)

print("distance (crossing meridian): %s" % p1.distance(p2))
print("-")


p1 = Position(-52.2296756, 1.0122287)
p2 = Position(-52.406374, -3.0748319)

print("distance (crossing equator): %s" % p1.distance(p2))
print("-")

