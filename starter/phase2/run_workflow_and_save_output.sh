#!/usr/bin/env bash
# Run the agentic workflow and save terminal output for submission.
#
# Usage: From the phase2 directory, run: bash run_workflow_and_save_output.sh
# Or from project root: bash starter/phase2/run_workflow_and_save_output.sh

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"
OUTPUT_FILE="${SCRIPT_DIR}/workflow_output.txt"

echo "Running agentic_workflow.py and saving output to: $OUTPUT_FILE"
echo "Command: python agentic_workflow.py" > "$OUTPUT_FILE"
echo "Output:" >> "$OUTPUT_FILE"
echo "-------" >> "$OUTPUT_FILE"
python agentic_workflow.py >> "$OUTPUT_FILE" 2>&1
echo "Done. Submit $OUTPUT_FILE (or a screenshot) as Phase 2 workflow evidence."
