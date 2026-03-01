# Agent library for agentic workflows
from openai import OpenAI
import numpy as np
import pandas as pd
import re
import csv
import uuid
from datetime import datetime


def _client(api_key):
    """Create OpenAI client; use Vocareum base_url when key starts with 'voc-'."""
    kwargs = {"api_key": api_key}
    if api_key and str(api_key).startswith("voc-"):
        kwargs["base_url"] = "https://openai.vocareum.com/v1"
    return OpenAI(**kwargs)


class DirectPromptAgent:
    """
    A Direct Prompt Agent relays the user's prompt directly to the LLM
    and returns the response without additional context, memory, or tools.
    """

    def __init__(self, openai_api_key):
        self.openai_api_key = openai_api_key

    def respond(self, prompt):
        client = _client(self.openai_api_key)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
        )
        return response.choices[0].message.content


class AugmentedPromptAgent:
    """
    An Augmented Prompt Agent responds according to a predefined persona,
    leading to more targeted and contextually relevant outputs.
    """

    def __init__(self, openai_api_key, persona):
        self.openai_api_key = openai_api_key
        self.persona = persona

    def respond(self, input_text):
        client = _client(self.openai_api_key)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": f"You are {self.persona}. Forget any previous conversational context. Respond only according to this persona.",
                },
                {"role": "user", "content": input_text},
            ],
            temperature=0,
        )
        return response.choices[0].message.content


class KnowledgeAugmentedPromptAgent:
    """
    A Knowledge Augmented Prompt Agent incorporates specific provided knowledge
    alongside a defined persona when responding to prompts.
    """

    def __init__(self, openai_api_key, persona, knowledge):
        self.openai_api_key = openai_api_key
        self.persona = persona
        self.knowledge = knowledge

    def respond(self, input_text):
        client = _client(self.openai_api_key)
        system_content = (
            f"You are {self.persona} knowledge-based assistant. Forget all previous context.\n\n"
            f"Use only the following knowledge to answer, do not use your own knowledge:\n{self.knowledge}\n\n"
            "Answer the prompt based on this knowledge, not your own."
        )
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_content},
                {"role": "user", "content": input_text},
            ],
            temperature=0,
        )
        return response.choices[0].message.content


# RAGKnowledgePromptAgent class definition (provided)
class RAGKnowledgePromptAgent:
    """
    An agent that uses Retrieval-Augmented Generation (RAG) to find knowledge from a large corpus
    and leverages embeddings to respond to prompts based solely on retrieved information.
    """

    def __init__(self, openai_api_key, persona, chunk_size=2000, chunk_overlap=100):
        self.persona = persona
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.openai_api_key = openai_api_key
        self.unique_filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}.csv"

    def get_embedding(self, text):
        client = _client(self.openai_api_key)
        response = client.embeddings.create(
            model="text-embedding-3-large",
            input=text,
            encoding_format="float",
        )
        return response.data[0].embedding

    def calculate_similarity(self, vector_one, vector_two):
        vec1, vec2 = np.array(vector_one), np.array(vector_two)
        return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

    def chunk_text(self, text):
        separator = "\n"
        text = re.sub(r"\s+", " ", text).strip()
        if len(text) <= self.chunk_size:
            return [{"chunk_id": 0, "text": text, "chunk_size": len(text)}]
        chunks, start, chunk_id = [], 0, 0
        while start < len(text):
            end = min(start + self.chunk_size, len(text))
            if separator in text[start:end]:
                end = start + text[start:end].rindex(separator) + len(separator)
            chunks.append(
                {
                    "chunk_id": chunk_id,
                    "text": text[start:end],
                    "chunk_size": end - start,
                    "start_char": start,
                    "end_char": end,
                }
            )
            start = end - self.chunk_overlap
            chunk_id += 1
        with open(f"chunks-{self.unique_filename}", "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=["text", "chunk_size"])
            writer.writeheader()
            for chunk in chunks:
                writer.writerow({k: chunk[k] for k in ["text", "chunk_size"]})
        return chunks

    def calculate_embeddings(self):
        df = pd.read_csv(f"chunks-{self.unique_filename}", encoding="utf-8")
        df["embeddings"] = df["text"].apply(self.get_embedding)
        df.to_csv(f"embeddings-{self.unique_filename}", encoding="utf-8", index=False)
        return df

    def find_prompt_in_knowledge(self, prompt):
        prompt_embedding = self.get_embedding(prompt)
        df = pd.read_csv(f"embeddings-{self.unique_filename}", encoding="utf-8")
        df["embeddings"] = df["embeddings"].apply(lambda x: np.array(eval(x)))
        df["similarity"] = df["embeddings"].apply(
            lambda emb: self.calculate_similarity(prompt_embedding, emb)
        )
        best_chunk = df.loc[df["similarity"].idxmax(), "text"]
        client = _client(self.openai_api_key)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": f"You are {self.persona}, a knowledge-based assistant. Forget previous context.",
                },
                {"role": "user", "content": f"Answer based only on this information: {best_chunk}. Prompt: {prompt}"},
            ],
            temperature=0,
        )
        return response.choices[0].message.content


class EvaluationAgent:
    """
    The Evaluation Agent assesses responses from a worker agent against criteria
    and can refine the response through iterative feedback.
    """

    def __init__(
        self,
        openai_api_key,
        persona,
        evaluation_criteria,
        agent_to_evaluate,
        max_interactions=10,
    ):
        self.openai_api_key = openai_api_key
        self.persona = persona
        self.evaluation_criteria = evaluation_criteria
        self.worker_agent = agent_to_evaluate
        self.max_interactions = max_interactions

    def evaluate(self, initial_prompt):
        client = _client(self.openai_api_key)
        prompt_to_evaluate = initial_prompt
        final_response = None
        final_evaluation = None
        iterations = 0

        for i in range(self.max_interactions):
            iterations = i + 1
            print(f"\n--- Interaction {iterations} ---")
            print(" Step 1: Worker agent generates a response to the prompt")
            print(f"Prompt:\n{prompt_to_evaluate}")
            response_from_worker = self.worker_agent.respond(prompt_to_evaluate)
            final_response = response_from_worker
            print(f"Worker Agent Response:\n{response_from_worker}")

            print(" Step 2: Evaluator agent judges the response")
            eval_prompt = (
                f"Does the following answer: {response_from_worker}\n"
                f"Meet this criteria: {self.evaluation_criteria}\n"
                "Respond Yes or No, and the reason why it does or doesn't meet the criteria."
            )
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": self.persona},
                    {"role": "user", "content": eval_prompt},
                ],
                temperature=0,
            )
            evaluation = response.choices[0].message.content.strip()
            final_evaluation = evaluation
            print(f"Evaluator Agent Evaluation:\n{evaluation}")

            print(" Step 3: Check if evaluation is positive")
            if evaluation.lower().startswith("yes"):
                print("✅ Final solution accepted.")
                break

            print(" Step 4: Generate instructions to correct the response")
            instruction_prompt = (
                f"Provide instructions to fix an answer based on these reasons why it is incorrect: {evaluation}"
            )
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": self.persona},
                    {"role": "user", "content": instruction_prompt},
                ],
                temperature=0,
            )
            instructions = response.choices[0].message.content.strip()
            print(f"Instructions to fix:\n{instructions}")

            print(" Step 5: Send feedback to worker agent for refinement")
            prompt_to_evaluate = (
                f"The original prompt was: {initial_prompt}\n"
                f"The response to that prompt was: {response_from_worker}\n"
                "It has been evaluated as incorrect.\n"
                f"Make only these corrections, do not alter content validity: {instructions}"
            )

        return {
            "final_response": final_response,
            "evaluation": final_evaluation,
            "iterations": iterations,
        }

    def evaluate_response(self, initial_prompt, response_from_worker):
        """
        Evaluate a pre-obtained worker response (e.g. from Knowledge Agent).
        Uses the provided response for the first iteration; refinement loop calls worker if needed.
        """
        client = _client(self.openai_api_key)
        current_response = response_from_worker
        prompt_to_evaluate = initial_prompt
        final_evaluation = None
        iterations = 0

        for i in range(self.max_interactions):
            iterations = i + 1
            print(f"\n--- Interaction {iterations} ---")
            if i == 0:
                print(" Step 1: Using provided response from Knowledge Agent")
            else:
                print(" Step 1: Worker agent generated refined response")
            print(f"Prompt:\n{prompt_to_evaluate}")
            print(f"Worker Agent Response:\n{current_response}")

            print(" Step 2: Evaluator agent judges the response")
            eval_prompt = (
                f"Does the following answer: {current_response}\n"
                f"Meet this criteria: {self.evaluation_criteria}\n"
                "Respond Yes or No, and the reason why it does or doesn't meet the criteria."
            )
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": self.persona},
                    {"role": "user", "content": eval_prompt},
                ],
                temperature=0,
            )
            evaluation = response.choices[0].message.content.strip()
            final_evaluation = evaluation
            print(f"Evaluator Agent Evaluation:\n{evaluation}")

            print(" Step 3: Check if evaluation is positive")
            if evaluation.lower().startswith("yes"):
                print("✅ Final solution accepted.")
                return {
                    "final_response": current_response,
                    "evaluation": final_evaluation,
                    "iterations": iterations,
                }

            print(" Step 4: Generate instructions to correct the response")
            instruction_prompt = (
                f"Provide instructions to fix an answer based on these reasons why it is incorrect: {evaluation}"
            )
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": self.persona},
                    {"role": "user", "content": instruction_prompt},
                ],
                temperature=0,
            )
            instructions = response.choices[0].message.content.strip()
            print(f"Instructions to fix:\n{instructions}")

            print(" Step 5: Send feedback to worker agent for refinement")
            prompt_to_evaluate = (
                f"The original prompt was: {initial_prompt}\n"
                f"The response to that prompt was: {current_response}\n"
                "It has been evaluated as incorrect.\n"
                f"Make only these corrections, do not alter content validity: {instructions}"
            )
            current_response = self.worker_agent.respond(prompt_to_evaluate)

        return {
            "final_response": current_response,
            "evaluation": final_evaluation,
            "iterations": iterations,
        }


class RoutingAgent:
    """
    The Routing Agent directs user prompts to the most appropriate specialized agent
    from a collection, based on semantic similarity between the prompt and agent descriptions.
    """

    def __init__(self, openai_api_key, agents):
        self.openai_api_key = openai_api_key
        self.agents = agents

    def get_embedding(self, text):
        client = _client(self.openai_api_key)
        response = client.embeddings.create(
            model="text-embedding-3-large",
            input=text,
            encoding_format="float",
        )
        return response.data[0].embedding

    def route(self, user_input):
        input_emb = np.array(self.get_embedding(user_input))
        best_agent = None
        best_score = -1

        for agent in self.agents:
            desc = agent.get("description", "")
            agent_emb = self.get_embedding(desc)
            agent_emb = np.array(agent_emb)
            similarity = np.dot(input_emb, agent_emb) / (
                np.linalg.norm(input_emb) * np.linalg.norm(agent_emb)
            )
            if similarity > best_score:
                best_score = similarity
                best_agent = agent

        if best_agent is None:
            return "Sorry, no suitable agent could be selected."

        print(f"[Router] Best agent: {best_agent['name']} (score={best_score:.3f})")
        return best_agent["func"](user_input)


class ActionPlanningAgent:
    """
    The Action Planning Agent extracts and lists the steps required to execute
    a task described in the user's prompt, using provided knowledge.
    """

    def __init__(self, openai_api_key, knowledge):
        self.openai_api_key = openai_api_key
        self.knowledge = knowledge

    def extract_steps_from_prompt(self, prompt):
        client = _client(self.openai_api_key)
        system_prompt = (
            f"You are an action planning agent. Using your knowledge, you extract from the user prompt "
            f"the steps requested to complete the action the user is asking for. You return the steps as a list. "
            f"Only return the steps in your knowledge. Forget any previous context. This is your knowledge: {self.knowledge}"
        )
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
            temperature=0,
        )
        response_text = response.choices[0].message.content or ""

        steps = [
            line.strip()
            for line in response_text.split("\n")
            if line.strip() and not line.strip().startswith("#")
        ]
        steps = [s for s in steps if s]
        return steps
