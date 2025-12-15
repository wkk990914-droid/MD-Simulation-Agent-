import os
from typing import Optional, Any
from langgraph_supervisor import create_supervisor
from agentframework.reasoning.llm_adapter import get_llm_instance
from agentframework.agent.conversational_agent import conversational_agent
from agentframework.agent.molecular_agent import molec_prep_agent
from agentframework.utils.formatter import pretty_print_messages

# 确保关键依赖导入失败时给出明确提示
try:
    from langgraph.graph import StateGraph
    # 在新版本中，CompiledGraph 已被 StateGraph 或其他类型替代
    CompiledGraph = StateGraph  # 使用 StateGraph 作为类型注解
except ImportError as e:
    raise ImportError(f"缺少langgraph依赖：{e}\n请安装：pip install langgraph")

def build_supervisor_agent() -> CompiledGraph:
    """
    构建监督者Agent（协调对话/分子模拟Agent）
    
    Returns:
        CompiledGraph: 编译后的监督者Agent实例
    """
    # 获取LLM实例并做有效性检查
    llm = get_llm_instance()
    if llm is None:
        raise ValueError("LLM实例初始化失败！请检查get_llm_instance()实现")
    
    # 验证Agent实例有效性
    if not hasattr(conversational_agent, "stream") or not hasattr(molec_prep_agent, "stream"):
        raise AttributeError("对话Agent/分子模拟Agent必须实现stream方法")
    
    # 构建监督者Agent
    supervisor = create_supervisor(
        model=llm,
        agents=[conversational_agent, molec_prep_agent],
        prompt=(
            "You are a supervisor managing two agents:\n"
            "- a conversational agent. Assign conversational tasks to this agent\n"
            "- a molecular simulation agent. Assign molecular simulation-related tasks to this agent\n"
            "Assign work to one agent at a time, do not call agents in parallel.\n"
            "Do not do any work yourself.\n"
            "Only return the result from the assigned agent, no additional explanation."
        ),
        add_handoff_back_messages=True,
        output_mode="full_history",
    )
    
    # 编译Graph并返回
    compiled_supervisor = supervisor.compile()
    return compiled_supervisor

# 全局监督者Agent实例（懒加载，避免启动时立即初始化）
_supervisor: Optional[CompiledGraph] = None

def get_supervisor_instance() -> CompiledGraph:
    """获取全局监督者Agent实例（单例模式）"""
    global _supervisor
    if _supervisor is None:
        _supervisor = build_supervisor_agent()
    return _supervisor

def supervisor_query(user_prompt: str) -> Optional[str]:
    """
    向监督者Agent发送用户指令，流式返回结果并格式化输出
    
    Args:
        user_prompt: 用户输入的指令文本
    
    Returns:
        Optional[str]: 监督者Agent最终返回的内容（失败返回None）
    """
    # 参数校验
    if not isinstance(user_prompt, str) or len(user_prompt.strip()) == 0:
        print("错误：用户指令不能为空！")
        return None
    
    supervisor = get_supervisor_instance()
    final_message_history: Optional[Any] = None
    
    try:
        # 流式处理Agent响应
        for chunk in supervisor.stream(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": user_prompt.strip(),
                    }
                ]
            }
        ):
            # 格式化打印更新信息
            pretty_print_messages(chunk, last_message=True)
            final_message_history = chunk
        
        # 提取最终响应内容（增加多层判空，避免KeyError）
        if (final_message_history and 
            isinstance(final_message_history, dict) and 
            "supervisor" in final_message_history and 
            isinstance(final_message_history["supervisor"], dict) and 
            "messages" in final_message_history["supervisor"] and 
            len(final_message_history["supervisor"]["messages"]) > 0):
            
            final_msg = final_message_history["supervisor"]["messages"][-1]
            return getattr(final_msg, "content", None) or str(final_msg)
        
        print("警告：未从监督者Agent获取到有效响应")
        return None
    
    except Exception as e:
        print(f"执行supervisor_query时出错：{type(e).__name__}: {e}")
        return None

supervisor = get_supervisor_instance()