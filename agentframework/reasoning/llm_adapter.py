from langchain.chat_models import init_chat_model
from langchain_ollama.chat_models import ChatOllama
from agentframework.config.llm_config import LLM_CONFIG

def get_llm_instance():
    """统一初始化LLM实例，适配不同模型类型"""
    if LLM_CONFIG["type"] == "ollama":
        return ChatOllama(**LLM_CONFIG["config"])
    # 可扩展：OpenAI/智谱等其他模型
    # elif LLM_CONFIG["type"] == "openai":
    #     return ChatOpenAI(**LLM_CONFIG["config"])
    else:
        raise ValueError(f"Unsupported LLM type: {LLM_CONFIG['type']}")