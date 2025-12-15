agent-framework/
├── agent/                      # Agent核心定义
│   ├── __init__.py
│   ├── base_agent.py           # （新增）Agent抽象基类
│   ├── conversational_agent.py # 对话Agent（conversational_agent定义）
│   └── molecular_agent.py      # 分子模拟Agent（molec_prep_agent定义）
├── multi_agent/                # 多Agent协作
│   ├── __init__.py
│   ├── supervisor.py           # 监督者Agent（supervisor定义+supervisor_query）
│   └── coordinator.py          # （新增）协作协调器基础逻辑
├── reasoning/                  # 决策层（LangGraph/LLM驱动）
│   ├── __init__.py
│   ├── llm_adapter.py          # LLM初始化（ChatOllama/init_chat_model）
│   └── react_strategy.py       # ReAct Agent构建（create_react_agent封装）
├── tools/                      # 工具层（分子模拟工具）
│   ├── __init__.py
│   ├── base_tool.py            # （新增）工具抽象基类
│   └── molecular_simulation/   # 分子模拟专用工具
│       ├── __init__.py
│       ├── mol_calculator.py   # molnum函数
│       ├── lammps_data.py      # gen_lammps_data函数
│       ├── lammps_input.py     # create_lammps_input_file函数
│       └── ensemble_analysis.py# ensemble_average函数
├── utils/                      # 通用工具
│   ├── __init__.py
│   ├── formatter.py            # pretty_print_message/messages函数
│   └── stream_utils.py         # （新增）流式输出辅助函数
├── config/                     # 配置层
│   ├── __init__.py
│   ├── llm_config.py           # Ollama/模型配置（地址、模型名）
│   └── default_config.yaml     # （可选）YAML配置文件
├── examples/                   # 示例代码
│   ├── __init__.py
│   ├── test_single_agent.py    # agent_1_response/agent_2_response测试
│   └── test_supervisor_agent.py # supervisor_query+所有prompt测试
├── requirements.txt            # 依赖清单
└── README.md                   # 框架说明