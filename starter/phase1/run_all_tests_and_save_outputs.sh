#!/usr/bin/env bash
# Run each of the 7 Phase 1 test scripts and save terminal output to a separate text file.
# Submit these output files (or screenshots of them) as evidence of successful test execution.
#
# Usage: From the phase1 directory, run: bash run_all_tests_and_save_outputs.sh
# Or from project root: bash starter/phase1/run_all_tests_and_save_outputs.sh

set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"
OUTPUT_DIR="${SCRIPT_DIR}/phase1_test_outputs"
mkdir -p "$OUTPUT_DIR"

# Use python3 if available (many environments don't have 'python'), else python
PYTHON_CMD=""
if command -v python3 &>/dev/null; then
    PYTHON_CMD="python3"
elif command -v python &>/dev/null; then
    PYTHON_CMD="python"
else
    echo "Error: neither python3 nor python found in PATH"
    exit 1
fi
echo "Using: $PYTHON_CMD"
echo "Running Phase 1 test scripts and saving outputs to: $OUTPUT_DIR"
echo ""

run_test() {
    local name="$1"
    local script="$2"
    local outfile="${OUTPUT_DIR}/${name}.txt"
    echo "=== Running $script ==="
    echo "Command: $PYTHON_CMD $script" > "$outfile"
    echo "Output:" >> "$outfile"
    echo "-------" >> "$outfile"
    # -u = unbuffered so output appears in file immediately
    if $PYTHON_CMD -u "$script" >> "$outfile" 2>&1; then
        echo "  -> Saved to $outfile"
    else
        echo "  -> Script exited with error; output saved to $outfile"
    fi
    echo ""
}

# run_test "01_direct_prompt_agent" "direct_prompt_agent.py"
# run_test "02_augmented_prompt_agent" "augmented_prompt_agent.py"
# run_test "03_knowledge_augmented_prompt_agent" "knowledge_augmented_prompt_agent.py"
run_test "04_rag_knowledge_prompt_agent" "rag_knowledge_prompt_agent.py"
# run_test "05_evaluation_agent" "evaluation_agent.py"
# run_test "06_routing_agent" "routing_agent.py"
# run_test "07_action_planning_agent" "action_planning_agent.py"

echo "Done. Submit the 7 files in $OUTPUT_DIR/ as evidence (or take screenshots of each)."
