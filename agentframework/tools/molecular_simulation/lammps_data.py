import os
### Define tool #2 - gen_lammps_data
# Function to create a data file for LAMMPS simulations using only 1 input. The input is a smiles string of a molecule.
def gen_lammps_data(name: str, smiles: str, box_size: float, n_molecs: int) -> str:
    """Function to create a data file for LAMMPS simulations using only 1 input. The input is a smiles string of a molecule."""
    import mbuild
    import foyer
    import warnings
    warnings.filterwarnings("ignore")

    # Define inputs
    system_smiles = smiles  ##'CCO'  # Ethanol for example
    box_size = box_size  # nano meter =
    n_molecules = n_molecs  # Number of molecules
    forcefield_name = 'oplsaa'  # OPLS-AA forcefield
    system_name = name  # Name of the system

    # Load system using its SMILES strings
    system_unparad = mbuild.load(system_smiles, smiles=True)
    system_unparad.name = system_name

    # build box
    box = mbuild.Box(3 * [box_size])

    # Fill the box with the molecule of interest
    filled_box = mbuild.fill_box(compound=system_unparad, n_compounds=n_molecules, box=box, overlap=0.2)

    # apply the forcefield to the system
    ff = foyer.Forcefield(name=forcefield_name)
    filled_box_param = filled_box.to_parmed(infer_residues=True)  # Parmed structure
    filled_box_parametrized = ff.apply(filled_box_param)  # ff applied

    # Pass the parametrized system to a Lammps data file in the generated_files directory
    mbuild.formats.lammpsdata.write_lammpsdata(
        filled_box_parametrized,
        os.path.join("generated_files", str(system_name) + ".data"),
        atom_style="full",
        unit_style="real",
        use_rb_torsions=True,
    )

    # Try except to catch errors
    try:
        return f"LAMMPS data file for {system_name} created successfully with {n_molecules} molecules. The box size is {box_size} nm. The file name is {system_name}.data"
    except Exception as e:
        return f"There was an error creating the LAMMPS data file: {str(e)}. Please check the inputs and try again."