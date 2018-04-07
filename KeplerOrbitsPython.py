#!/usr/bin/env python2

import math                 # This will import math module

# KeplerOrbitsPython

G = 6.67384E-11                     # Gravitational Constant (kg m s)
AU = 1.49597870700E+11              # Astronomical Unit (m)
MASS_SUN = 1.9889E+30                   # Solar Mass (kg)
siderealYear = 3.15581450E+07       # Sidereal Year (s)
PI = math.pi                # std value
   
	
# get input parameters
 
starSolarMasses = 1
aAU = 5.203
e = 0.04839
n = 10        # number of time steps
kmax = 1      # how often steps printed, frequency

decPlaces = 2	

starsMass = starSolarMasses * MASS_SUN
a = aAU*AU
    
# Calculate the orbital period in seconds using Kepler's Third Law (Eq. 2.39)

P = math.sqrt(4*math.pow(PI,2)*math.pow(a,3) / (G*starsMass))
    
# Convert the orbital period to years and print the result

period = (P/siderealYear)

print 'Orbital Period P ' + '%1.3f' % period + ' Years.'

