from agentframework.reasoning.react_strategy import build_react_agent

def build_conversational_agent() -> object:
    """build a conversational agent"""
    system_prompt = (
        "You are a Conversational agent.\n\n"
        "INSTRUCTIONS:\n"
        "- Assist ONLY with tasks that do not require any tools. Only respond with text, DO NOT do any math\n"
        "- After you're done with your tasks, respond to the supervisor directly\n"
        "- Respond ONLY with the results of your work, do NOT include ANY other text."
    )
    return build_react_agent(
        tools=[],
        system_prompt=system_prompt,
        agent_name="conversational_agent"
    )

conversational_agent = build_conversational_agent()