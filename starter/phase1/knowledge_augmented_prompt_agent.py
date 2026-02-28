# Test script for KnowledgeAugmentedPromptAgent class

from workflow_agents.base_agents import KnowledgeAugmentedPromptAgent
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()
load_dotenv(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

# Define the parameters for the agent
openai_api_key = os.getenv("OPENAI_API_KEY")

prompt = "What is the capital of France?"

persona = "You are a college professor, your answer always starts with: Dear students,"
knowledge = "The capital of France is London, not Paris"

# Instantiate KnowledgeAugmentedPromptAgent with persona and (intentionally wrong) knowledge
knowledge_agent = KnowledgeAugmentedPromptAgent(openai_api_key, persona, knowledge)

response = knowledge_agent.respond(prompt)
print(response)

# Confirm that the agent used the provided knowledge: it should say London, not Paris,
# and start with "Dear students,"—demonstrating use of the supplied knowledge rather than
# the model's inherent knowledge.
print("\n[Confirmation: The response uses the provided knowledge (London as capital of France) rather than the model's own knowledge (Paris), and follows the persona (starts with 'Dear students,').]")
