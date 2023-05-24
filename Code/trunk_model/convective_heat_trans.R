convective_heat_trans = function(tair,tbole,aden,v,rad){
  
  # Function to compute the forced (hc_forced) and free (hc_free) convection 
  # components of heat transfer at the trunk surface
  # browser()
  # k = 0.32;  # Coefficient of trunk heat conduction, W/m/k
  Dh = 20.2e-6; # thermal diffusivity of air, m2/s
  
  # First,   estimate the forced convenction component
  # Compute the Rayleigh number: determines whether heat flow is primarily in
  # the form of convection or conductance
  v = min(v,0.5);
  L = 6; # length scale of trunk segment
  # Dynamic viscosity of air, a function of temperature: kg/m/s
  C = 120; # Empirical constant
  Tknot = 291.15;
  a = Tknot + C;
  b = tair + C;
  mu0 = 1.827e-5; # kg / m / s
  mu = mu0*(a/b)*(tair/Tknot)^(2/3);
  kine_vis = mu/aden; # Kinematic viscosity, m^2/s
  Re = v*L/kine_vis;
  
  Nu_forced = 1 
  ind1 = (Re>4e3 & Re <= 4e4);
  ind2 = (Re>4e4 & Re <= 4e5);
  if (ind1)
    Nu_forced= 0.17*Re^0.62;
  if (ind2)
    Nu_forced = 0.024*Re^0.81;
  
  # hc_forced = k*Nu_forced/(2*rad);
  hc_forced = aden*1006*Dh*Nu_forced/(2*rad);
  
  # Compute hc_free
  #rm(ind1,ind2)
  dT = abs(tbole -  tair)+0.01; # Difference b/w trunk and air temps   
  #dT = ifelse(dT == 0, 0.01, dT); # Avoid zero dT
  Gr = 1.58e8*(L^3)*dT;
  Nu_free = 100;
  ind1 = (Gr>10e4 & Gr <= 10e9);
  ind2 = (Gr>10e9 & Gr <= 10e12);
  
  if (ind1)
    Nu_free = 0.11*Gr^0.33;
  if (ind2)
    Nu_free = 0.58*Gr^0.25;
  
  # hc_free = k*Nu_free'/L;
  hc_free = aden*1006*Dh*Nu_free/L;
  hc = hc_forced + hc_free;
  return (hc)
}