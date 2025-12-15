### Define tool #1 - molnum
# Function to determine number of molecules required for a given cubic box size and density
def molnum(dens: float, mm: float, lx: float) -> int:
    """Function to determine number of molecules required for a given cubic box size and density"""
    ly = lz = lx  # cubic box
    # Determine volume of the simulation box and change to m
    vol_a = lx * ly * lz  ##A^3

    ## 1 A = 10^-7 m
    arm = 10**(-10)  # m
    vol_m = vol_a * arm**3  ##m^3

    # Use inputs to determine molarity (mol/cm3)
    molarity_cm = dens / mm  # mol/cm3
    molarity_m = molarity_cm * (100**3)  # mol/m3

    # Define avogadro's number
    Na = 6.022 * (10**23)  ## particle/mol

    # Determine the number of molecules and print results
    num = molarity_m * vol_m * Na

    return round(num)