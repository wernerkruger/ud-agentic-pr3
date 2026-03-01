# Submission Artifacts – How to Generate and What to Submit

## Phase 1: Seven separate test script outputs

**Requirement:** One clear output artifact per test script (screenshot or text file), showing **command + prompt + response** for each of the seven scripts.

### How to generate the 7 Phase 1 outputs

1. Ensure `OPENAI_API_KEY` is set in a `.env` file at the **project root** (or in `starter/phase1/`).
2. From the project root, run:
   ```bash
   cd starter/phase1
   bash run_all_tests_and_save_outputs.sh
   ```
3. This creates the folder `starter/phase1/phase1_test_outputs/` with 7 text files:
   - `01_direct_prompt_agent.txt` – includes prompt, response, and **knowledge source** explanation
   - `02_augmented_prompt_agent.txt` – includes prompt, response, and **knowledge/persona** discussion
   - `03_knowledge_augmented_prompt_agent.txt` – includes prompt, response, and **confirmation** of provided knowledge use
   - `04_rag_knowledge_prompt_agent.txt`
   - `05_evaluation_agent.txt`
   - `06_routing_agent.txt`
   - `07_action_planning_agent.txt`

4. **Submit** these 7 files (or screenshots of each) so reviewers can see:
   - The command used
   - The prompt (when printed by the script)
   - The agent’s response
   - For Direct/Augmented/KnowledgeAugmented: the required explanatory/confirmation lines

---

## Phase 2: Workflow output

**Requirement:** Evidence of the workflow run showing the **final consolidated output** with user stories, product features, and engineering tasks.

### How to generate the Phase 2 output

1. From the project root:
   ```bash
   cd starter/phase2
   bash run_workflow_and_save_output.sh
   ```
2. This creates `starter/phase2/workflow_output.txt` containing the full run, including:
   - Workflow prompt (full-plan: user stories + features + tasks)
   - Steps and routing
   - **Final consolidated output** with sections: **USER STORIES**, **PRODUCT FEATURES**, **ENGINEERING TASKS**

3. **Submit** this file (or a screenshot) as Phase 2 workflow evidence.

---

## Checklist before submitting

- [ ] **Phase 1:** 7 separate outputs (text files or screenshots), one per test script.
- [ ] **Phase 1:** DirectPromptAgent output includes the “knowledge source” print.
- [ ] **Phase 1:** AugmentedPromptAgent output includes the “knowledge/persona impact” print.
- [ ] **Phase 1:** KnowledgeAugmentedPromptAgent output includes the “confirmation” print.
- [ ] **Phase 2:** Workflow output shows the **consolidated** final plan (user stories + features + tasks), not only the last step.
