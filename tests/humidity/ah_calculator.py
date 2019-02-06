#!/usr/bin/env python3

"""
Created on 4 Feb 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

https://www.aqua-calc.com/calculate/humidity
https://carnotcycle.wordpress.com/2012/08/04/how-to-convert-relative-humidity-to-absolute-humidity/
https://planetcalc.com/2167/
"""

import math


# --------------------------------------------------------------------------------------------------------------------

rh = 60
t = 25

print("t: %s rh: %s" % (t, rh))
print("=")


tk = t + 273.15

tck = 647.096

pc = 22064000

a1 = -7.85951783
a2 = 1.84408259
a3 = -11.7866497
a4 = 22.6807411
a5 = -15.9618719
a6 = 1.80122502

rw = 461.52

# where:  Pws is saturated water vapor pressure,
# Pc is critical pressure equal to 22.064 MPa,
# Tc is critical temperature equal to 647.096 K,
# ϑ = (1 − T ⁄ Tc),

# --------------------------------------------------------------------------------------------------------------------
# technique 1: https://www.aqua-calc.com/calculate/humidity

# ϑ = (1 − (T ⁄ Tc)),

theta = 1 - (tk / tck)

print("theta: %s" % theta)
print("-")


# ln(Pws ⁄ Pc) = Tc ⁄ T × (a1 × ϑ + a2 × ϑ1.5+ a3 × ϑ3+ a4 × ϑ3.5+ a5 × ϑ4+ a6 × ϑ7.5)

thetas = (a1 * theta) + (a2 * pow(theta, 1.5)) + (a3 * pow(theta, 3)) + (a4 * pow(theta, 3.5)) + \
         (a5 * pow(theta, 4)) + (a6 * pow(theta, 7.5))

print("thetas: %s" % thetas)
print("-")


ln_pws_pc = (tck / tk) * thetas

print("ln_pws_pc: %s" % ln_pws_pc)
print("-")


pws = math.exp(ln_pws_pc) * pc

print("pws: %s" % pws)
print("-")


# Pw = RH × Pws  ⁄  100

pw = pws * (rh / 100)

print("pw: %s" % pw)
print("-")


# AH, kg/m³ = Pw  ⁄  (Rw × T)

ah = pw / (rw * tk)

print("ah1: %s" % ah)
print("=")


# --------------------------------------------------------------------------------------------------------------------
# technique 2: https://carnotcycle.wordpress.com/2012/08/04/how-to-convert-relative-humidity-to-absolute-humidity/

p_sat = 6.112 * math.exp((17.67 * t) / (t + 243.5))

p = p_sat * (rh / 100)

wv_moles = p / (tk * 0.083136)

wv_grammes = wv_moles * 18.02

ah = wv_grammes / 1000

print("ah2: %s" % ah)
print("-")
