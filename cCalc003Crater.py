
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

Cd = new Array(3)      # regular array (add an optional integer
Cd[0] = 1.88;          # argument to control array's size)
Cd[1] = 1.54;
Cd[2] = 1.6;

var beta = new Array(3);
beta[0] = 0.22;
beta[1] = 0.165;
beta[2] = 0.22;

var gEarth = 9.8;    // gravity acceleration earth
var gmoon = 1.67;    // gravity acceleration moon
var m = 0;           // projectile mass
var dscale = 0;      // scale for crater diameter
var anglefac = 0;    // impact angle factor
var densfac = 0;     // density factor

var rhomoon = 2700;  // density moon
var Dstarmoon = 1.8e4; //
var Dstar = 0;         // transition crater
var Dsimple = 0;       //
var Dpr = 0;           // peak ring crater diameter
var Dprmoon = 1.4e5;   //
var Dfinal = 0;        // crater type transient (0) or final (1)
var Dpiscale = 0;      // piscale result
var Dyield = 0;        // yield scaling result
var Dgault = 0;        // gault scaling result
var gsmall = 0;        // gault scale calc
var Tform = 0;         // crater formation time
var Lpiscale = 0;      // piscale result
var Lyield = 0;        // yield scale result
var Lgault = 0;        // gault scaling result
# var ans not used can be re run on web page
var cratertype = "";   // crater type description
var targtype = 0;      // target type 0, 1, 2
# var comptype not used - separated calculations
var ejectaSpread = 0;



# get input parameters

    L = document.inputDataView1.input4.value;   
    v = document.inputDataView1.input5.value;  
    targetDensity = document.inputDataView1.input6.value; 
    projectileDensity = document.inputDataView1.input10.value; 
    theta = document.inputDataView1.input11.value;  
    g = document.inputDataView1.input12.value;  
    effectRadius = document.inputDataView1.input14.value;
    decPlaces = document.inputDataView1.input16.value;
    targtype = document.inputDataView1.input18.value;  
    
  
# if targtype < 1 etc
 
# convert units to SI and compute some auxiliary quantites

    v = 1000 * v               # km sec to m sec
    craterDiam = 1000 * craterDiam;                      //km to m
    Dfinal = 1000 * Dfinal;              //km to m
    theta = theta * (pi / 180);            //degrees to radians
    anglefac = Math.pow(Math.sin(theta),third);      //impact angle factor
    densfac = Math.pow(projectileDensity,0.16667) / Math.sqrt(targetDensity);
    pifac = (1.61 * g)  /  (v * v);             //inverse froude length factor
    Ct = 0.80;                           //coefficient for formation time

    if(targtype == 1) {
        Ct = 1.3;
    }
    
Dstar = (gmoon * rhomoon * Dstarmoon) / (g * targetDensity) # transition crater diameter
Dpr = (gmoon * rhomoon * Dprmoon  ) / (g * targetDensity) # peak-ring crater Diameter


# ***********************************************************************

#          computation for specified projectile diameter

# ***********************************************************************

    m = (pi / 6) * projectileDensity * L * L * L;  # projectile mass
    
# Projectile Kinetic Energy prior to entry into Atmosphere - Equation 1*

    projectileKE = 0.5 * m * v * v;                  
      
# Number of near Earth asteroids with Diameter > L - Equation 2*

    nL = 1148 * Math.pow(L / 1000, -2.354);
    
    
    pitwo = pifac * L ;                  //inverse froude number
    dscale = Math.pow((m/targetDensity),third ) ;   //scale for crater diameter


//    Pi Scaling (Schmidt and Holsapple 1987)

    Dpiscale = dscale * Cd[targtype] * Math.pow(pitwo,-beta[targtype]);
    Dpiscale = Dpiscale * anglefac;


//    Yield Scaling (Nordyke 1962) with small correction for depth
//     of projectile penetration

    Dyield = 0.0133 * Math.pow(projectileKE,(1 / 3.4)) + 1.51 * Math.sqrt(projectileDensity / targetDensity) * L;
    Dyield = Dyield * anglefac * Math.pow((gEarth / g),0.165);


//     Gault (1974) Semi-Empirical scaling

    gsmall = 0.25 * densfac * Math.pow(projectileKE,0.29) * anglefac;
        
        
    if(targtype == 2) {
        gsmall = 0.015 * densfac * Math.pow(projectileKE,0.37) * Math.pow(anglefac,2);
    }
        

    if(gsmall < 100) {
        Dgault = gsmall;
    } else {
        Dgault = 0.27 * densfac * Math.pow(projectileKE,0.28) * anglefac;
    }
       
    Dgault = Dgault * Math.pow((gmoon / g),0.165);

//    Compute crater formation time from Schmidt and Housen

    Tform = (Ct * L / v) * Math.pow(pitwo,-0.61);

//     Compute final crater type and diameter from pi-scaled transient dia.

    Dsimple = 1.56 * Dpiscale;
     
    if (Dsimple < Dstar) {
	      Dfinal = Dsimple;
	      cratertype = "Simple";
	  } else {
        Dfinal = Math.pow(Dsimple,1.18) / Math.pow(Dstar,0.18);
	      cratertype = "Complex";
	  }
		

	  if(Dsimple < Dstar * 1.4 && Dsimple > Dstar * 0.71) {
        cratertype = "Simple/Complex";
    }
         
	  if(Dfinal > Dpr) {
	      cratertype = "Peak-ring";
    }

// continEjectaBlanket Dfinal + Dfinal

    continEjectaBlanket = Dfinal + Dfinal;

// Calculate ejecta spread at 2.15 x final crater diameter

    ejectaSpread = Dfinal  * 2.15;  

    
// Calculate impactor volume from diameter assuming spherical

    impactorVolume = (4/3) * pi * Math.pow((L/2),3);

// Calculate impactor mass from density and volume

    impactorMass = impactorVolume * projectileDensity;

// Calculate Seismic magnitude at impact site - Equation 40*

//     M = 0.67 *  (Math.log(projectileKE) / Math.LN10) - 5.87;
   
    M = 0.67 * Math.antilog(projectileKE) - 5.87;

// Calculate Seismic effect at radius r km from impact
    mEff = M - 0.0238 * effectRadius;
 

// function outPutResults() {

// Output Results grid on outputResultView1

    var outputResult1 = new Number(impactorVolume);
    document.outputResultView1.result1.value = outputResult1.toExponential(decPlaces);

//  document.outputResultView1.result2.value = ;

    document.outputResultView1.result3.value = cratertype;

    var outputResult4 = new Number(impactorMass);
    document.outputResultView1.result4.value = outputResult4.toExponential(decPlaces);

    var outputResult5 = new Number(Dyield);
    document.outputResultView1.result5.value = outputResult5.toExponential(decPlaces);

    var outputResult6 = new Number(continEjectaBlanket);
    document.outputResultView1.result6.value = outputResult6.toExponential(decPlaces)

    var outputResult7 = new Number(projectileKE);
    document.outputResultView1.result7.value = outputResult7.toExponential(decPlaces);
    
    var outputResult8 = new Number(Dpiscale);
    document.outputResultView1.result8.value = outputResult8.toExponential(decPlaces);
    
    var outputResult9 = new Number(ejectaSpread);
    document.outputResultView1.result9.value = outputResult9.toExponential(decPlaces);

    var outputResult10 = new Number(projectileKE * 2.387665e-16);
    document.outputResultView1.result10.value = outputResult10.toExponential(decPlaces);


    var outputResult11 = new Number(Dgault);
    document.outputResultView1.result11.value = outputResult11.toExponential(decPlaces);

    var outputResult12 = new Number(M);
    document.outputResultView1.result12.value = outputResult12.toExponential(decPlaces);

    var outputResult13 = new Number(nL);
    document.outputResultView1.result13.value = outputResult13.toExponential(0);

    var outputResult15 = new Number(mEff);
    document.outputResultView1.result15.value = outputResult15.toExponential(2);
    
    var outputResult17 = new Number(Dfinal);
    document.outputResultView1.result17.value = outputResult17.toExponential(2);

//  document.outputResultView1.result19.value = ;

    var outputResult20 = new Number(Tform);
    document.outputResultView1.result20.value = outputResult20.toExponential(2);
 
//  document.outputResultView1.result21.value = ;
//  document.outputResultView1.result22.value = ;
//  document.outputResultView1.result23.value = ;
//  document.outputResultView1.result24.value = ;

}


function openDiagWindow() {

// used to display values at various stages of calculation for verification
// that formulas are translated correctly, using electronic calculator

    diagWindow = window.open("","Diagnostics -","toolbar=no, location=no, directories=no, status=no,menubar=no, scrollbars=no, resizable=no, copyhistory=yes, width=350, height=350");
  
 //   diagWindow = window.open();
    diagWindow.document.open();
    diagWindow.document.write("<title>Diagnostics</title>");
    diagWindow.document.write("<pre>Diagnostic Window  :<p/>");
    diagWindow.document.write("projectileDensity = ",projectileDensity,"<br/>");
    diagWindow.document.write("targetDensity     = ",targetDensity,"<br/>");
    diagWindow.document.write("L                 = ",L,"<br/>");
    diagWindow.document.write("v                 = ",v,"<br/>");
    diagWindow.document.write("theta             = ",theta,"<br/>");
    diagWindow.document.write("anglefac          = ",anglefac,"<br/>");
    diagWindow.document.write("densfac           = ",densfac,"<br/>");
    diagWindow.document.write("pifac             = ",pifac,"<br/>");
    diagWindow.document.write("Ct                = ",Ct,"<br/>");
    diagWindow.document.write("Dstar             = ",Dstar,"<br/>");
    diagWindow.document.write("Dpr               = ",Dpr,"<br/>");
    diagWindow.document.write("m                 = ",m,"<br/>");
    diagWindow.document.write("projectileKE      = ",projectileKE,"<br/>");
    diagWindow.document.write("pitwo             = ",pitwo,"<br/>");
    diagWindow.document.write("dscale            = ",dscale,"<br/>");
    diagWindow.document.write("gsmall            = ",gsmall,"<br/>");
    diagWindow.document.write("cratertype        = ",cratertype,"<br/>");
    diagWindow.document.write("</pre>");
    diagWindow.focus();

}