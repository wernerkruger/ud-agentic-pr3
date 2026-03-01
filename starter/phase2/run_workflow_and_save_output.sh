#!/usr/bin/env bash
# Run the agentic workflow and save terminal output for submission.
#
# Usage: From the phase2 directory, run: bash run_workflow_and_save_output.sh
# Or from project root: bash starter/phase2/run_workflow_and_save_output.sh

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"
OUTPUT_FILE="${SCRIPT_DIR}/workflow_output.txt"

if command -v python3 &>/dev/null; then
    PYTHON_CMD="python3"
elif command -v python &>/dev/null; then
    PYTHON_CMD="python"
else
    echo "Error: neither python3 nor python found"
    exit 1
fi

echo "Running agentic_workflow.py and saving output to: $OUTPUT_FILE"
echo "Command: $PYTHON_CMD agentic_workflow.py" > "$OUTPUT_FILE"
echo "Output:" >> "$OUTPUT_FILE"
echo "-------" >> "$OUTPUT_FILE"
$PYTHON_CMD -u agentic_workflow.py >> "$OUTPUT_FILE" 2>&1
echo "Done. Submit $OUTPUT_FILE (or a screenshot) as Phase 2 workflow evidence."
