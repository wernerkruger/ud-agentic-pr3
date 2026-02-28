# agentic_workflow.py
# Agentic workflow for technical project management (Email Router pilot)

from workflow_agents.base_agents import (
    ActionPlanningAgent,
    KnowledgeAugmentedPromptAgent,
    EvaluationAgent,
    RoutingAgent,
)

import os
from dotenv import load_dotenv

# Load environment variables (try current dir and project root)
load_dotenv()
script_dir = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(script_dir, "..", "..", ".env"))

# Load the OpenAI API key
openai_api_key = os.getenv("OPENAI_API_KEY")

# Load the product spec document
spec_path = os.path.join(script_dir, "Product-Spec-Email-Router.txt")
with open(spec_path, "r", encoding="utf-8") as f:
    product_spec = f.read()

# ---------------------------------------------------------------------------
# Action Planning Agent
# ---------------------------------------------------------------------------
knowledge_action_planning = (
    "Stories are defined from a product spec by identifying a "
    "persona, an action, and a desired outcome for each story. "
    "Each story represents a specific functionality of the product "
    "described in the specification. \n"
    "Features are defined by grouping related user stories. \n"
    "Tasks are defined for each story and represent the engineering "
    "work required to develop the product. \n"
    "A development Plan for a product contains all these components"
)
action_planning_agent = ActionPlanningAgent(openai_api_key, knowledge_action_planning)

# ---------------------------------------------------------------------------
# Product Manager - Knowledge Augmented Prompt Agent
# ---------------------------------------------------------------------------
persona_product_manager = "You are a Product Manager, you are responsible for defining the user stories for a product."
knowledge_product_manager = (
    "Stories are defined by writing sentences with a persona, an action, and a desired outcome. "
    "The sentences always start with: As a "
    "Write several stories for the product spec below, where the personas are the different users of the product. \n\n"
    + product_spec
)
product_manager_knowledge_agent = KnowledgeAugmentedPromptAgent(
    openai_api_key, persona_product_manager, knowledge_product_manager
)

# ---------------------------------------------------------------------------
# Product Manager - Evaluation Agent
# ---------------------------------------------------------------------------
persona_pm_eval = "You are an evaluation agent that checks the answers of other worker agents"
evaluation_criteria_pm = (
    "The answer should be stories that follow the following structure: "
    "As a [type of user], I want [an action or feature] so that [benefit/value]."
)
product_manager_evaluation_agent = EvaluationAgent(
    openai_api_key,
    persona_pm_eval,
    evaluation_criteria_pm,
    product_manager_knowledge_agent,
    max_interactions=10,
)

# ---------------------------------------------------------------------------
# Program Manager - Knowledge Augmented Prompt Agent
# ---------------------------------------------------------------------------
persona_program_manager = "You are a Program Manager, you are responsible for defining the features for a product."
knowledge_program_manager = "Features of a product are defined by organizing similar user stories into cohesive groups."
program_manager_knowledge_agent = KnowledgeAugmentedPromptAgent(
    openai_api_key, persona_program_manager, knowledge_program_manager
)

# ---------------------------------------------------------------------------
# Program Manager - Evaluation Agent
# ---------------------------------------------------------------------------
persona_program_manager_eval = "You are an evaluation agent that checks the answers of other worker agents."
evaluation_criteria_program = (
    "The answer should be product features that follow the following structure: "
    "Feature Name: A clear, concise title that identifies the capability\n"
    "Description: A brief explanation of what the feature does and its purpose\n"
    "Key Functionality: The specific capabilities or actions the feature provides\n"
    "User Benefit: How this feature creates value for the user"
)
program_manager_evaluation_agent = EvaluationAgent(
    openai_api_key,
    persona_program_manager_eval,
    evaluation_criteria_program,
    program_manager_knowledge_agent,
    max_interactions=10,
)

# ---------------------------------------------------------------------------
# Development Engineer - Knowledge Augmented Prompt Agent
# ---------------------------------------------------------------------------
persona_dev_engineer = "You are a Development Engineer, you are responsible for defining the development tasks for a product."
knowledge_dev_engineer = "Development tasks are defined by identifying what needs to be built to implement each user story."
development_engineer_knowledge_agent = KnowledgeAugmentedPromptAgent(
    openai_api_key, persona_dev_engineer, knowledge_dev_engineer
)

# ---------------------------------------------------------------------------
# Development Engineer - Evaluation Agent
# ---------------------------------------------------------------------------
persona_dev_engineer_eval = "You are an evaluation agent that checks the answers of other worker agents."
evaluation_criteria_dev = (
    "The answer should be tasks following this exact structure: "
    "Task ID: A unique identifier for tracking purposes\n"
    "Task Title: Brief description of the specific development work\n"
    "Related User Story: Reference to the parent user story\n"
    "Description: Detailed explanation of the technical work required\n"
    "Acceptance Criteria: Specific requirements that must be met for completion\n"
    "Estimated Effort: Time or complexity estimation\n"
    "Dependencies: Any tasks that must be completed first"
)
development_engineer_evaluation_agent = EvaluationAgent(
    openai_api_key,
    persona_dev_engineer_eval,
    evaluation_criteria_dev,
    development_engineer_knowledge_agent,
    max_interactions=10,
)

# ---------------------------------------------------------------------------
# Support functions for routed tasks (each calls Knowledge Agent then Evaluation Agent)
# ---------------------------------------------------------------------------


def product_manager_support_function(query):
    """Get user stories from Product Manager agent and validate via Evaluation Agent."""
    result = product_manager_evaluation_agent.evaluate(query)
    return result["final_response"]


def program_manager_support_function(query):
    """Get product features from Program Manager agent and validate via Evaluation Agent."""
    result = program_manager_evaluation_agent.evaluate(query)
    return result["final_response"]


def development_engineer_support_function(query):
    """Get engineering tasks from Development Engineer agent and validate via Evaluation Agent."""
    result = development_engineer_evaluation_agent.evaluate(query)
    return result["final_response"]


# ---------------------------------------------------------------------------
# Routing Agent (routes steps to Product Manager, Program Manager, or Development Engineer)
# ---------------------------------------------------------------------------
routing_routes = [
    {
        "name": "Product Manager",
        "description": "Responsible for defining product personas and user stories only. Does not define features or tasks. Does not group stories.",
        "func": product_manager_support_function,
    },
    {
        "name": "Program Manager",
        "description": "Responsible for defining product features by grouping user stories. Does not define individual user stories or engineering tasks.",
        "func": program_manager_support_function,
    },
    {
        "name": "Development Engineer",
        "description": "Responsible for defining detailed engineering tasks and development work for each user story. Does not define user stories or features.",
        "func": development_engineer_support_function,
    },
]
routing_agent = RoutingAgent(openai_api_key, routing_routes)

# ---------------------------------------------------------------------------
# Run the workflow
# ---------------------------------------------------------------------------

print("\n*** Workflow execution started ***\n")

workflow_prompt = "What would the development tasks for this product be?"
print(f"Task to complete in this workflow, workflow prompt = {workflow_prompt}")

print("\nDefining workflow steps from the workflow prompt")
workflow_steps = action_planning_agent.extract_steps_from_prompt(workflow_prompt)

completed_steps = []
for i, step in enumerate(workflow_steps, 1):
    print(f"\n{'='*60}")
    print(f"Step {i}: {step}")
    print("=" * 60)
    result = routing_agent.route(step)
    completed_steps.append(result)
    print(f"\nResult for step {i}:")
    print(result)

print("\n" + "=" * 60)
print("*** Final output of the workflow ***")
print("=" * 60)
if completed_steps:
    print(completed_steps[-1])
else:
    print("No steps were completed.")
