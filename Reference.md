python3 -m venv .venv
source .venv/bin/activate
pip3 install python-dotenv


pip install pyautogen python-dotenv


pip3 install -U "autogen-agentchat" "autogen-ext[openai]"


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

