# Test script for DirectPromptAgent class

from workflow_agents.base_agents import DirectPromptAgent
import os
from dotenv import load_dotenv

# Load environment variables from .env file (current dir or project root)
load_dotenv()
load_dotenv(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

# Load the OpenAI API key from the environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")

prompt = "What is the Capital of France?"
print("Prompt:", prompt)
print()

# Instantiate the DirectPromptAgent and send the prompt
direct_agent = DirectPromptAgent(openai_api_key)
direct_agent_response = direct_agent.respond(prompt)

# Print the response from the agent
print("Response:", direct_agent_response)

# The agent uses only the general knowledge encoded in the selected LLM model (gpt-3.5-turbo).
# No system prompt, external knowledge, or memory is used—only the user prompt is sent to the model.
print("\n[Knowledge source: The agent used only the general knowledge of the gpt-3.5-turbo model; no system prompt or external knowledge was provided.]")
