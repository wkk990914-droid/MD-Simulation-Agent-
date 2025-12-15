OLLAMA_CONFIG = {
    "model": "qwen3:30b",
    "base_url": "http://192.168.31.94:11434"
}

# 可扩展支持多模型配置
LLM_CONFIG = {
    "type": "ollama",
    "config": OLLAMA_CONFIG
}