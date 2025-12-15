Agent Framework for Molecular Simulation Automation
<img width="86" height="20" alt="image" src="https://github.com/user-attachments/assets/bc7082e5-4c89-4efa-b679-467d083de32d" />
<img width="108" height="20" alt="image" src="https://github.com/user-attachments/assets/8ecf4f89-ebe4-41ee-8b8b-e8cae2e3920e" />
<img width="112" height="20" alt="image" src="https://github.com/user-attachments/assets/e1dea0fe-e9d2-4e69-a046-32ee58037d8b" />
<img width="240" height="20" alt="image" src="https://github.com/user-attachments/assets/77d77c8b-6ff2-447e-8dbc-a7216de95b7e" />
<img width="895" height="153" alt="image" src="https://github.com/user-attachments/assets/726a9e6c-89ee-4ce8-9eba-f460f315819b" />


Project Structure
agent-framework/
├── agent/                  # Core Agent Definitions
│   ├── __init__.py
│   ├── base_agent.py       # Abstract base class for all agents (defines core interfaces)
│   ├── conversational_agent.py  # Conversational agent for user interaction
│   └── molecular_agent.py  # Specialized agent for molecular simulation tasks (solvent config, LAMMPS runs)
├── multi_agent/            # Multi-Agent Collaboration Logic
│   ├── __init__.py
│   ├── supervisor.py       # Supervisor agent (coordinates sub-agents, handles task routing)
│   └── coordinator.py      # Base logic for agent collaboration coordination
├── reasoning/              # LLM & Reasoning Layer (LangGraph/ReAct Strategy)
│   ├── __init__.py
│   ├── llm_adapter.py      # LLM initialization (ChatOllama/ChatOpenAI, model config)
│   └── react_strategy.py   # Encapsulates ReAct agent construction for task reasoning
├── tools/                  # Domain-Specific Tools for Molecular Simulation
│   ├── __init__.py
│   ├── base_tool.py        # Abstract base class for custom tools
│   └── molecular_simulation/  # Molecular simulation tooling
│       ├── __init__.py
│       ├── mol_calculator.py  # Molecular property calculation (molnum function)
│       ├── lammps_data.py     # LAMMPS data file generation (gen_lammps_data function)
│       ├── lammps_input.py    # LAMMPS input file creation (create_lammps_input_file function)
│       └── ensemble_analysis.py # Trajectory ensemble average analysis (ensemble_average function)
├── utils/                  # Utility Functions
│   ├── __init__.py
│   ├── formatter.py        # Message formatting (pretty_print_message, messages helper)
│   └── stream_utils.py     # Stream output utilities for LLM responses
├── config/                 # Configuration Management
│   ├── __init__.py
│   ├── llm_config.py       # Ollama/OpenAI model configuration (address, model name)
│   └── default_config.yaml # Optional YAML config file (editable for custom paths/models)
├── examples/               # Example Scripts for Testing
│   ├── __init__.py
│   ├── test_single_agent.py # Test single agent (molecular/conversational) responses
│   └── test_supervisor_agent.py # Test multi-agent supervisor query and prompt logic
├── requirements.txt        # Project Dependencies
└── README.md               # Framework Documentation (this file)

