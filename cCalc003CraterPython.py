import math

# Short program to evaluate the scaling equations to determine
# the diameter of a transient crater given details on the nature
# of the projectile, conditions of impact, and state of the
# target.  The diameter is evaluated by three independent methods,
# yield scaling, pi-scaling and Gault's semi-empirical relations
# supplemented by rules on how crater size depends on gravity and
# angle of impact.

# Updated Nov. 1997 to compute projectile size from a given
# transient crater diameter.  Projectile and crater diameter
# computation functions merged into a single program April 1998.
# See Melosh, Impact Cratering, chapter 7 for more details

# Updated Oct. 1999 to take final crater diameters as well as 
# transient crater diameters into account.

# Copyright 1996, 1997 and 1998 by H. J. Melosh, adapted with authors
# permission.
# Python version 2015 Alchymist's Laboratory

#  define all Global variables

Ct = 0                 # Formation time coefficient
craterDiam = 0         # Crater diameter in km
dStd = 0               # craterDiam divided by anglefac
L = 0                  # Projectile diameter in m
projectileDensity = 0  # Projectile density kg m3
v = 0                  # Projectile velocity km s
theta = 0              # Impact angle in degrees
targetDensity = 0      # Target density kg m3
g = 0                  # gravity acceleration m s2
projectileKE = 0       # projectile Kinetic Energy


pi = 3.15145   # use Pi from cConstants.js library under common code
third = 1/3
pitwo = 0      # inverse froude number
pifac = 0      # inverse froude length number


# constants for the Schmidt-Holsapple pi scaling and gravity conversion factors

Cd = [1.88,1.54,1.6]      # list (like array) refer to by Cd[0], Cd[1] etc

beta = [0.22,0.165,0.22]

gEarth = 9.8    # gravity acceleration earth
gmoon = 1.67  # gravity acceleration moon
m = 0          # projectile mass
dscale = 0     # scale for crater diameter
anglefac = 0   # impact angle factor
densfac = 0     # density factor

rhomoon = 2700  # density moon
Dstarmoon = 1.8e4
Dstar = 0         #  transition crater
Dsimple = 0      
Dpr = 0          # peak ring crater diameter
Dprmoon = 1.4e5
Dfinal = 0       # crater type transient (0) or final (1)
Dpiscale = 0      # piscale result
Dyield = 0      # yield scaling result
Dgault = 0   # gault scaling result
gsmall = 0       # gault scale calc
Tform = 0        # crater formation time
Lpiscale = 0      # piscale result
Lyield = 0        # yield scale result
Lgault = 0       # gault scaling result
# var ans not used can be re run on web page
cratertype = ""   # crater type description
targtype = 0      # target type 0, 1, 2
# var comptype not used - separated calculations
ejectaSpread = 0



# input parameters - Meteor Crater USA example

L = 40.0
v = 20000  
targetDensity = 2500 # Kg m-3
projectileDensity = 8000 
theta = 0.787  
g = 9.18 
effectRadius = 10
decPlaces = 2
targtype = 2  
    
  
# if targtype < 1 etc
 
# convert units to SI and compute some auxiliary quantites

v = 1000 * v               # km sec to m sec
craterDiam = 1000 * craterDiam                      # km to m
Dfinal = 1000 * Dfinal             # km to m
theta = theta * (pi / 180)        # degrees to radians
anglefac = pow(math.sin(theta),third) # impact angle factor
densfac = pow(projectileDensity,0.16667) / math.sqrt(targetDensity)
pifac = (1.61 * g)  /  (v * v)           # inverse froude length factor
Ct = 0.80                       # coefficient for formation time

if targtype == 1 : 
        Ct = 1.3

Dstar = (gmoon * rhomoon * Dstarmoon) / (g * targetDensity) # transition crater diameter
Dpr = (gmoon * rhomoon * Dprmoon  ) / (g * targetDensity) # peak-ring crater Diameter


# ***********************************************************************

#          computation for specified projectile diameter

# ***********************************************************************

m = (pi / 6) * projectileDensity * L * L * L  # projectile mass
    
# Projectile Kinetic Energy prior to entry into Atmosphere - Equation 1*

projectileKE = 0.5 * m * v * v                
      
# Number of near Earth asteroids with Diameter > L - Equation 2*

# nL = 1148 * math.pow(L / 1000, -2.354) - gives error in Python
# for negative powers e.g. x^-2 the equivalent is 1/x^2

nL = 1148 * (1 / math.pow(L / 1000, 2.354))
    
pitwo = pifac * L     # inverse froude number
dscale = pow((m/targetDensity),third ) # scale for crater diameter


#     Pi Scaling (Schmidt and Holsapple 1987)

Dpiscale = dscale * Cd[targtype] * math.pow(pitwo,-beta[targtype])
Dpiscale = Dpiscale * anglefac


#     Yield Scaling (Nordyke 1962) with small correction for depth
#     of projectile penetration

Dyield = 0.0133 * pow(projectileKE,(1 / 3.4)) + 1.51 * math.sqrt(projectileDensity / targetDensity) * L
Dyield = Dyield * anglefac * pow((gEarth / g),0.165)


#     Gault (1974) Semi-Empirical scaling

gsmall = 0.25 * densfac * pow(projectileKE,0.29) * anglefac
        
        
if targtype == 2 :
    gsmall = 0.015 * densfac * pow(projectileKE,0.37) * pow(anglefac,2);
    
        

if gsmall < 100 :
    Dgault = gsmall
else:
    Dgault = 0.27 * densfac * pow(projectileKE,0.28) * anglefac;

       
Dgault = Dgault * pow((gmoon / g),0.165)

#     Compute crater formation time from Schmidt and Housen

Tform = (Ct * L / v) * pow(pitwo,-0.61)

#      Compute final crater type and diameter from pi-scaled transient dia.

Dsimple = 1.56 * Dpiscale
     
if Dsimple < Dstar :
	  Dfinal = Dsimple
	  cratertype = "Simple"
else:
        Dfinal = pow(Dsimple,1.18) / pow(Dstar,0.18)
	cratertype = "Complex"

		

if Dsimple < Dstar * 1.4 :
    if Dsimple > Dstar * 0.71 :
        cratertype = "Simple/Complex"
    
         
if Dfinal > Dpr :
	 cratertype = "Peak-ring"
    

#  continEjectaBlanket Dfinal + Dfinal

continEjectaBlanket = Dfinal + Dfinal

#  Calculate ejecta spread at 2.15 x final crater diameter

ejectaSpread = Dfinal  * 2.15

    
#  Calculate impactor volume from diameter assuming spherical

impactorVolume = (4/3) * pi * pow((L/2),3)

#  Calculate impactor mass from density and volume

impactorMass = impactorVolume * projectileDensity

#  Calculate Seismic magnitude at impact site - Equation 40*

#      M = 0.67 *  (Math.log(projectileKE) / Math.LN10) - 5.87;
#  AntiLog(X) = 10^X or 10**X   
# M = 0.67 * math.antilog(projectileKE) - 5.87

M = 0.67 * 10**projectileKE - 5.87

#  Calculate Seismic effect at radius r km from impact

mEff = M - 0.0238 * effectRadius
 


print(impactorVolume)

print(cratertype)

print(impactorMass)
print(Dyield)
print(continEjectaBlanket)

print(projectileKE)
    
print(Dpiscale)
    
print(ejectaSpread)
 
print(projectileKE * 2.387665e-16)


print(Dgault)
print(M)

print(nL)

print(mEff)
    
print(Dfinal)

#   document.outputResultView1.result19.value = ;

print(Tform)




print('Diagnostics')

print('projectileDensity = ' + projectileDensity)
print('targetDensity     = ' + targetDensity)
print('L                 = ' + L)
print('v                 = ' + v)
print('theta             = ' + theta)
print('anglefac          = ' + anglefac)
print('densfac           = ' + densfac)
print('pifac             = ' + pifac)
print('Ct                = ' + Ct)
print('Dstar             = ' + Dstar)
print('Dpr               = ' + Dpr)
print('m                 = ' + m)
print('projectileKE      = ' + projectileKE)
print('pitwo             = ' + pitwo)
print('dscale            = ' + dscale)
print('gsmall            = ' + gsmall)
print('cratertype        = ' + cratertype)

