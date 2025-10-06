python3 -m venv .venv
source .venv/bin/activate
pip3 install python-dotenv


pip install pyautogen python-dotenv
pip install -U "autogen-agentchat" "autogen-ext[openai]"


1. Basic single agent - Simple task execution
2. Tool integration - Adding custom functions as tools
3. Multi-modal input - Working with images
4. Two-agent interaction - Basic multi-agent patterns
5. Structured output - Using Pydantic models for typed responses
6. Streaming - Real-time token output
7. Multiple tool iterations - Complex reasoning chains


Advanced concepts
8. Round Robin Teams - Agents take turns in fixed order with reflection pattern
9. Selector Group Chat - AI-driven speaker selection based on context
10. Custom Memory Management - Control conversation history per agent
11. Agent-as-Tool - Using specialized agents as callable functions
12. Sequential Handoffs - Workflow with explicit handoff between stages
13. External Control - Stopping teams externally and cancellation
14. State Management - Resuming conversations and managing team state



Building Blocks of AutoGen 
===
  Agents
  Models
  Tools
  Terminations

Key features of AutoGen 
====
  1. Asynchronous Messaging
  2. Scalable & Distributed
  3. Multi-Language Support
  4. Modular & Extensible
  5. Observable & Debuggable
  6. Event-Driven Architecture



AI Agent Patterns
====
  1. Tool Use Pattern 
      (example2)
      AI agents can identify and call tools to connect to external apis, databases, etc.

  2. Reflection Pattern 
      (example9)

      AI Agents evaluate AI agent's own output and reflect -- till it arrives at final response

  3. Agent as Tool Pattern 
      (example11)

      Sometimes tools should connect to LLM (example scenario: for fact checking)

  4. ReAct (Reasoning + Act) Pattern 
      Agent must show reasoning steps and then act. So that transparency is achieved 
      about decision making.

  5. Multi-Agent Pattern
      Some complex problems can be fixed when multiple agents aligned to 
      complete the tasks

  6. Planning Pattern 
      Agent will decompose the complex steps into small sub steps 
      



AI Agent Processes
===
    1. Sequential
    2. Hierachical
    3. Hybrid 
    4. Parallel
    5. Async