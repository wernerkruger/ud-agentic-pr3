# Test script for RoutingAgent class

from workflow_agents.base_agents import KnowledgeAugmentedPromptAgent, RoutingAgent
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
load_dotenv(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

openai_api_key = os.getenv("OPENAI_API_KEY")

# Texas Knowledge Augmented Prompt Agent
persona_texas = "You are a college professor"
knowledge_texas = "You know everything about Texas"
texas_agent = KnowledgeAugmentedPromptAgent(openai_api_key, persona_texas, knowledge_texas)

# Europe Knowledge Augmented Prompt Agent
knowledge_europe = "You know everything about Europe"
europe_agent = KnowledgeAugmentedPromptAgent(openai_api_key, persona_texas, knowledge_europe)

# Math Knowledge Augmented Prompt Agent
persona_math = "You are a college math professor"
knowledge_math = "You know everything about math, you take prompts with numbers, extract math formulas, and show the answer without explanation"
math_agent = KnowledgeAugmentedPromptAgent(openai_api_key, persona_math, knowledge_math)

# Routing agent with list of agents (name, description, func)
routing_agent = RoutingAgent(openai_api_key, [])
agents = [
    {
        "name": "texas agent",
        "description": "Answer a question about Texas",
        "func": lambda x: texas_agent.respond(x),
    },
    {
        "name": "europe agent",
        "description": "Answer a question about Europe",
        "func": lambda x: europe_agent.respond(x),
    },
    {
        "name": "math agent",
        "description": "When a prompt contains numbers, respond with a math formula",
        "func": lambda x: math_agent.respond(x),
    },
]
routing_agent.agents = agents

# Test routing with the required prompts
test_prompts = [
    "Tell me about the history of Rome, Texas",
    "Tell me about the history of Rome, Italy",
    "One story takes 2 days, and there are 20 stories",
]

for p in test_prompts:
    print(f"\n--- Prompt: {p} ---")
    print(routing_agent.route(p))
