from agentframework.reasoning.react_strategy import build_react_agent
from agentframework.tools.molecular_simulation.mol_calculator import molnum
from agentframework.tools.molecular_simulation.lammps_data import gen_lammps_data
from agentframework.tools.molecular_simulation.lammps_input import create_lammps_input_file
from agentframework.tools.molecular_simulation.ensemble_analysis import ensemble_average

def build_molecular_agent() -> object:
    """构建分子模拟Agent（绑定所有分子模拟工具）"""
    system_prompt = (
        "You are a Molecular simulation agent.\n\n"
        "INSTRUCTIONS:\n"
        "- Assist ONLY with tasks related to molecular Dynamics and use relevant tools, DO NOT do any math\n"
        "- After you're done with your tasks, respond to the supervisor directly\n"
        "- Respond ONLY with the results of your work, do NOT include ANY other text."
    )
    # 绑定工具
    tools = [molnum, gen_lammps_data, create_lammps_input_file, ensemble_average]
    return build_react_agent(
        tools=tools,
        system_prompt=system_prompt,
        agent_name="molec_prep_agent"
    )

# 全局实例
molec_prep_agent = build_molecular_agent()