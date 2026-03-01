from workflow_agents.base_agents import RAGKnowledgePromptAgent
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
load_dotenv(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

# Define the parameters for the agent
openai_api_key = os.getenv("OPENAI_API_KEY")
openai_api_key = 'voc-335810259159874469028369a31e3dd91616.44164269'

persona = "You are a college professor, your answer always starts with: Dear students,"
# Use larger chunk_size so short knowledge fits in one chunk (avoids heavy embedding/memory use)
RAG_knowledge_prompt_agent = RAGKnowledgePromptAgent(openai_api_key, persona, chunk_size=2000, chunk_overlap=100)

# Short knowledge (single chunk) to avoid many API calls and heavy numpy/pandas work that can crash the IDE.
# Still contains the answer for the prompt below.
knowledge_text = """
Clara is a marine biologist and science communicator in Boston. Inspired by her family's resilience,
she created a podcast called "Crosscurrents" that explores the intersection of science, culture, and ethics.
She interviews researchers, engineers, and artists. In one episode she explored how RAG could help
researchers find niche studies. Her life and work show the power of connecting across disciplines.
"""

chunks = RAG_knowledge_prompt_agent.chunk_text(knowledge_text)
RAG_knowledge_prompt_agent.calculate_embeddings()

prompt = "What is the podcast that Clara hosts about?"
print("Prompt:", prompt)
print()
prompt_answer = RAG_knowledge_prompt_agent.find_prompt_in_knowledge(prompt)
print("Response:", prompt_answer)
