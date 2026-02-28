# Test script for ActionPlanningAgent class

from workflow_agents.base_agents import ActionPlanningAgent
import os
from dotenv import load_dotenv

# Load environment variables and define the OpenAI API key
load_dotenv()
load_dotenv(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))
openai_api_key = os.getenv("OPENAI_API_KEY")

knowledge = """
# Fried Egg
1. Heat pan with oil or butter
2. Crack egg into pan
3. Cook until white is set (2-3 minutes)
4. Season with salt and pepper
5. Serve

# Scrambled Eggs
1. Crack eggs into a bowl
2. Beat eggs with a fork until mixed
3. Heat pan with butter or oil over medium heat
4. Pour egg mixture into pan
5. Stir gently as eggs cook
6. Remove from heat when eggs are just set but still moist
7. Season with salt and pepper
8. Serve immediately

# Boiled Eggs
1. Place eggs in a pot
2. Cover with cold water (about 1 inch above eggs)
3. Bring water to a boil
4. Remove from heat and cover pot
5. Let sit: 4-6 minutes for soft-boiled or 10-12 minutes for hard-boiled
6. Transfer eggs to ice water to stop cooking
7. Peel and serve
"""

# Instantiate ActionPlanningAgent with API key and knowledge
action_planning_agent = ActionPlanningAgent(openai_api_key, knowledge)

# Get and print the extracted steps for the prompt
steps = action_planning_agent.extract_steps_from_prompt(
    "One morning I wanted to have scrambled eggs"
)
print("Extracted action steps:")
for i, step in enumerate(steps, 1):
    print(f"  {i}. {step}")
