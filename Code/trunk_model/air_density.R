#replace % comment: "\% ([A-Z]){1}" with "# \1"
#replace . operator: "\.([\*|/|\^]){1}" with "\1"

aden  = function(tair,rh,p){
  # Function to compute air density from temperature, pressure & relative humidity
  # Air density is provided in units of kg/m^3
  
  # Define constants:
    Rd=287;         # Ideal gas constant of dry air (J/kg/K)
    Rv=461;         # Ideal gas constant of water vapor (J/kg/K)
    epsilon=Rd/Rv;  # Rd/Rv (-)
    e_s0=611;       # Reference staurated vapor pressure in
    # Clausius-Clapeyron Equation (Pa)
    T_0=273.15;     # Reference temperature in Clausius-Clapeyron Equatioin (K)
    Lv=2.5e6;       # Latent heat of vaporization (J/kg)
    
    # Compute saturated vapor pressure using the Clausius-Clapeyron Equation
    e_s = e_s0*exp(Lv/Rv*(1/T_0-(1/tair))); # in Pa
    # Determine vapor pressure
    ea = (rh*e_s)/100; # in Pa
    T_v = tair/(1-(1-epsilon)*(ea/(p*100))); # Virtual temperature (K)
    aden = (p*100)/(Rd*T_v); # Density of air in kg/m^3
    
    return (aden)
}

