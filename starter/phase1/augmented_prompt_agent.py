# Test script for AugmentedPromptAgent class

from workflow_agents.base_agents import AugmentedPromptAgent
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
load_dotenv(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

# Retrieve OpenAI API key from environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")

prompt = "What is the capital of France?"
persona = "You are a college professor; your answers always start with: 'Dear students,'"
print("Prompt:", prompt)
print()

# Instantiate AugmentedPromptAgent with API key and persona
augmented_agent = AugmentedPromptAgent(openai_api_key, persona)

# Send the prompt to the agent and store the response
augmented_agent_response = augmented_agent.respond(prompt)

# Print the agent's response
print("Response:", augmented_agent_response)

# Required: explanatory output for knowledge source and persona impact (visible in terminal/output)
print("\n[Knowledge source and persona impact: The agent used general LLM knowledge (e.g., Paris as capital of France) but formatted its answer according to the persona (college professor, starting with 'Dear students,'). Specifying the persona in the system prompt constrained the style and framing of the output, making it more contextually appropriate for the defined role.]")
