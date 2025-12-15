from langgraph.prebuilt import create_react_agent
from agentframework.reasoning.llm_adapter import get_llm_instance

def build_react_agent(tools: list, system_prompt: str, agent_name: str) -> object:
    """封装ReAct Agent构建逻辑，统一入参"""
    llm = get_llm_instance()
    return create_react_agent(
        model=llm,
        tools=tools,
        prompt=system_prompt,
        name=agent_name
    )