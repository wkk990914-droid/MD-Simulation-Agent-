import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, PROJECT_ROOT)

from agentframework.multi_agent.supervisor import supervisor_query
from IPython.display import display, Image

# 可视化Supervisor图
from agentframework.multi_agent.supervisor import supervisor
display(Image(supervisor.get_graph().draw_mermaid_png()))

# 测试用例
if __name__ == "__main__":
    # 测试Tool 1
    prompt_test_1 = "How many ethanol molecules are needed  in a cubic box of size 30 Angstroms for a density of 0.789 g/cm3. The molar mass is 46.07 g/mol."
    final_message_history = supervisor_query(prompt_test_1)

    # 测试Tool 2
    prompt_test_2 = "Generate LAMMPS data file for a molecular system using the smiles string. The inputs are the name of the molecule, smiles string, box size and number of molecules. Name: Ethanol, SMILES: CCO, Box size: 3.0 nm, Number of molecules: 250"
    final_message_history = supervisor_query(prompt_test_2)

    # 测试Tool 3
    prompt_test_3 = "Create a LAMMPS input file for a molecular system using the LAMMPSdata file called Ethanol.data and set the temperature to 300 K and pressure to 1 atm. The name of the input file should be Ethanol_npt.in"
    final_message_history = supervisor_query(prompt_test_3)

    # 测试Tool 4
    prompt_test_4 = "Analyze the convergence of the Density in a LAMMPS log file called '/home/wangkai/MD Simulation Agent/agentframework/log.lammps'. Use a tolerance of 0.1 and a window size of 50 timesteps. Save the plot as a PNG file."
    final_message_history = supervisor_query(prompt_test_4)