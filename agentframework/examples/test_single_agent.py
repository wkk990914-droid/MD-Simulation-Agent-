import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, PROJECT_ROOT)

from agentframework.agent.conversational_agent import conversational_agent
from agentframework.agent.molecular_agent import molec_prep_agent
from agentframework.utils.formatter import pretty_print_messages

def agent_1_response(input_text: str):
    for chunk in conversational_agent.stream(
        {"messages": [{"role": "user", "content": input_text}]}
    ):
        pretty_print_messages(chunk)

def agent_2_response(input_text: str):
    for chunk in molec_prep_agent.stream(
        {"messages": [{"role": "user", "content": input_text}]}
    ):
        pretty_print_messages(chunk)


if __name__ == "__main__":
    conv_1_test = "Hello, with what tasks can you assist me today?"
    agent_1_response(conv_1_test)

    prompt_test_1 = "How many ethanol molecules are needed  in a cubic box of size 30 Angstroms for a density of 0.789 g/cm3. The molar mass is 46.07 g/mol."
    agent_2_response(prompt_test_1)

    prompt_test_2 = "Generate LAMMPS data file for a molecular system using the smiles string. The inputs are the name of the molecule, smiles string, box size and number of molecules. Name: Ethanol, SMILES: CCO, Box size: 3.0 nm, Number of molecules: 250"
    agent_2_response(prompt_test_2)

    prompt_test_3 = "Create a LAMMPS input file for a molecular system using the LAMMPSdata file called Ethanol.data and set the temperature to 300 K and pressure to 1 atm. The name of the input file should be Ethanol_npt.in"
    agent_2_response(prompt_test_3)

    prompt_test_4 = "Analyze the convergence of the Density in a LAMMPS log file called '/home/wangkai/MD Simulation Agent/agentframework/log.lammps'. Use a tolerance of 0.1 and a window size of 50 timesteps. Save the plot as a PNG file."
    agent_2_response(prompt_test_4)
