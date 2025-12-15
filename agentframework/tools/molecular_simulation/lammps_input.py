### Tool 3: generate lammps input file 
## Function to create a lammps input file for a given molecule/system using its LAMMPS data file.
def create_lammps_input_file(input_file: str, data_file: str, Temp: float = 298.0, Pres: float = 1.0) -> str:
    """
    Create a LAMMPS input file for a given molecule/system using its LAMMPS data file.
    Args:
        input_file: Name of the input file to create (without .in extension)
        data_file: Name of the LAMMPS data file (with .data extension)
        Temp: Temperature in Kelvin (default: 298.0)
        Pres: Pressure in atm (default: 1.0)
    """
    import os
    try:
        with open(os.path.join('generated_files', f'{input_file}.inp'), 'w') as file:
            file.write(f'''
atom_style full
units real
boundary p p p
pair_style lj/cut/coul/long 12.0
kspace_style pppm 1.0e-4
bond_style harmonic
angle_style harmonic
dihedral_style opls

# ----------------- Atom Definition Section -----------------
read_data "{data_file}"

thermo 100

#  -- minimize -- (Minimization without fix shake)
minimize 1.0e-5 1.0e-7 1000 10000
reset_timestep 0
write_data system_minimized.data

# ----------------- Run Section -----------------              
# Setup timestep
timestep        1 #fs

# Define thermo output
thermo          1000
thermo_style    custom step time temp pe ke etotal enthalpy press lx vol density

#Create initial velocity distribution
velocity   all create {Temp} 097865 dist gaussian

## Fix commands
fix 1 all npt temp {Temp} {Temp} 100 iso {Pres} {Pres} 1000.0

# Define Dumping
#dump 1 all xyz 1000 test.xyz
dump 3 all dcd 1000 npt_trajectory.dcd

run 1000000 # 1 ns

write_data system_npt_equil.data
''')
        return f"Lammps input file {input_file}.inp created successfully."
    except Exception as e:
        return f"Error creating Lammps input file {input_file}.inp: {str(e)}."