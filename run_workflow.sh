#!/bin/bash
# Complete Fine-Tuning Workflow Script

set -e  # Exit on error

# Color codes for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}═════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}  PEFT Complete Fine-Tuning Workflow${NC}"
echo -e "${BLUE}═════════════════════════════════════════════════════════${NC}\n"

# Configuration
TAXONOMY_PATH="instructlab/taxonomy"
PIPELINE_OUTPUT="./pipeline_output"
TESTSET_FILE="peft_evaluation/example_testset.json"
BASELINE_PORT=8000
TRAINED_PORT=8001

# Step 1: Generate Data with Pipeline
echo -e "${YELLOW}1️⃣  Generating synthetic data with quality gates...${NC}"
python peft_pipeline/data_generation_pipeline.py \
    "$TAXONOMY_PATH" \
    --output "$PIPELINE_OUTPUT" \
    --num-instructions 500 \
    --rouge-threshold 0.75 \
    --quality-threshold 0.7

echo -e "${GREEN}✅ Data generation complete${NC}\n"

# Step 2: Train Model
echo -e "${YELLOW}2️⃣  Training model...${NC}"
echo -e "     Run: ${BLUE}ilab model train${NC}"
echo -e "     (This step requires manual execution or uncomment below)"
# ilab model train
echo -e "${GREEN}✅ Training step (manual)${NC}\n"

# Step 3: Convert Model
echo -e "${YELLOW}3️⃣  Converting model...${NC}"
echo -e "     Run: ${BLUE}ilab model convert${NC}"
echo -e "     (This step requires manual execution or uncomment below)"
# ilab model convert
echo -e "${GREEN}✅ Conversion step (manual)${NC}\n"

# Step 4: Quality Analysis of Generated Data
echo -e "${YELLOW}4️⃣  Analyzing generated data quality...${NC}"
for data_file in "$PIPELINE_OUTPUT"/*/generated/*.json; do
    if [ -f "$data_file" ]; then
        echo -e "     Analyzing: $(basename $(dirname $(dirname "$data_file")))"
        python peft_metrics/data_quality_analyzer.py "$data_file" > /dev/null
    fi
done
echo -e "${GREEN}✅ Quality analysis complete${NC}\n"

# Step 5: Inference Testing (if models are running)
echo -e "${YELLOW}5️⃣  Model Inference Testing (optional)${NC}"
echo -e "     Prerequisites:"
echo -e "     1. Baseline model running on http://localhost:$BASELINE_PORT/v1"
echo -e "     2. Trained model running on http://localhost:$TRAINED_PORT/v1"
echo -e ""
echo -e "     Start models in separate terminals:"
echo -e "     ${BLUE}ilab serve --model-path models/baseline.gguf${NC}"
echo -e "     ${BLUE}ilab serve --model-path models/trained/model.gguf --port $TRAINED_PORT${NC}"
echo -e ""
read -p "     Are both models running? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    python peft_evaluation/inference_tester.py \
        --baseline "http://localhost:$BASELINE_PORT/v1" \
        --trained "http://localhost:$TRAINED_PORT/v1" \
        --testset "$TESTSET_FILE" \
        --output "comparison_results.json"
    echo -e "${GREEN}✅ Model comparison complete${NC}\n"
    echo -e "     Results saved to: ${BLUE}comparison_results.json${NC}"
else
    echo -e "${YELLOW}⏭️  Skipping inference testing${NC}\n"
fi

# Summary
echo -e "${BLUE}═════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}✅ Workflow Summary${NC}"
echo -e "${BLUE}═════════════════════════════════════════════════════════${NC}"
echo -e "Pipeline Output:       $PIPELINE_OUTPUT"
echo -e "Generated Data Files:  $(find "$PIPELINE_OUTPUT" -name 'generated/*.json' 2>/dev/null | wc -l) files"
echo -e "Test Results:          comparison_results.json"
echo -e ""
echo -e "📊 Next Steps:"
echo -e "  1. Review quality metrics in pipeline_output/pipeline_report.txt"
echo -e "  2. Train model: ${BLUE}ilab model train${NC}"
echo -e "  3. Convert model: ${BLUE}ilab model convert${NC}"
echo -e "  4. Run inference testing with trained model"
echo -e "  5. Review results: ${BLUE}cat comparison_results.json${NC}"
echo -e "${BLUE}═════════════════════════════════════════════════════════${NC}\n"
