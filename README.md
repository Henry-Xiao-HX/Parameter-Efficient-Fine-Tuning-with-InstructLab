# PEFT with InstructLab

Parameter-efficient fine-tuning toolkit with data quality analysis, automated pipeline orchestration, and model evaluation.

**Version**: 2.0 | **Status**: Actively Maintained

---

## Contents

- [Architecture](#architecture)
- [Requirements](#requirements)
- [Quick Start](#quick-start)
- [Tools](#tools)
- [Workflow](#workflow)
- [Metrics](#metrics)
- [Roadmap](#roadmap)
- [Troubleshooting](#troubleshooting)

---

## Architecture

### System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    PEFT Fine-Tuning Framework               │
└─────────────────────────────────────────────────────────────┘
                              │
                ┌─────────────┼─────────────┐
                │             │             │
                ▼             ▼             ▼
        ┌──────────────┐ ┌──────────────┐ ┌─────────────────┐
        │   PHASE 1    │ │   PHASE 2    │ │    PHASE 3      │
        │ Data Prep    │ │   Training   │ │   Evaluation    │
        └──────────────┘ └──────────────┘ └─────────────────┘
                │             │             │
        ┌───────┴───────┐     │     ┌───────┴──────────┐
        │               │     │     │                  │
        ▼               ▼     ▼     ▼                  ▼
    ┌────────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────┐
    │  Synthetic │ │   Data   │ │  Adapter │ │  Inference   │
    │    Data    │ │ Quality  │ │ Training │ │   Tester     │
    │ Generation │ │ Analyzer │ │          │ │              │
    └────────────┘ └──────────┘ └──────────┘ └──────────────┘
         ▲             ▲             ▲             ▲
         │             │             │             │
    InstructLab      PEFT Metrics   InstructLab   PEFT Eval
```

### Component Breakdown

#### Phase 1: Data Preparation
- **Input**: Seed examples in `qna.yaml`
- **Process**: Generate synthetic training data using InstructLab
- **Output**: JSON/JSONL files with generated Q&A pairs
- **Tool**: [`peft_pipeline/data_generation_pipeline.py`](peft_pipeline/data_generation_pipeline.py)

#### Phase 2: Quality Analysis & Training
- **Input**: Generated synthetic data
- **Process**: 
  - Analyze data quality (duplicates, diversity, consistency)
  - Apply quality gates
  - Train adapter models using parameter-efficient techniques
- **Output**: Quality report, adapter files
- **Tools**: [`peft_metrics/data_quality_analyzer.py`](peft_metrics/data_quality_analyzer.py)

#### Phase 3: Evaluation & Comparison
- **Input**: Baseline and trained models, test cases
- **Process**: Run inference on both models and compare metrics
- **Output**: Accuracy improvements, latency metrics, domain-specific analysis
- **Tool**: [`peft_evaluation/inference_tester.py`](peft_evaluation/inference_tester.py)

## Roadmap

**v2.0** (Current) ✅
- `peft_metrics/`: Core quality analysis (metrics, deduplication, scoring, reporting)
- `peft_evaluation/`: Model inference comparison (accuracy, latency, domain-specific)

**v2.1** 🚧 WIP
- `peft_pipeline/`: Data orchestration (domain discovery, quality gates) + optimization

**v2.2+** 📋 Planned
- Advanced analysis: Statistical analysis, outlier detection, clustering, benchmarking
- Pipeline: Resume capability, incremental generation, dependency resolution
- Evaluation: Ensemble comparison, token-level accuracy, hallucination detection
- Integration: Web UI, MLflow tracking, optimization recommendations
- Performance: GPU acceleration, distributed processing, streaming

---

### Directory Structure

```
repository/
├── peft_metrics/                          # Data quality analysis
│   ├── data_quality_analyzer.py          # Main analyzer (✅ Complete)
│   ├── data_quality_analyzer_with_HuggingFace.py  # HF Evaluate version
│   ├── data_and_algo.md                  # Algorithm documentation
│   └── example_testset.json
├── peft_pipeline/                         # Data generation orchestration
│   ├── data_generation_pipeline.py       # Pipeline orchestrator (🚧 WIP)
│   └── __init__.py
├── peft_evaluation/                       # Model inference testing
│   ├── inference_tester.py               # Comparison tool (✅ Complete)
│   └── example_testset.json              # Sample test cases
├── models/                                # Model storage
│   ├── 2024_oscars/                      # Example domain
│   │   ├── generated/                    # Generated training data
│   │   ├── oscar/                        # Original QNA files
│   │   └── README.md
│   ├── finance_life_coach/               # Another example domain
│   └── baseline.gguf                     # Base model
├── QUICK_START.md                        # Quick reference
├── TOOLS_GUIDE.md                        # Detailed tool documentation
├── PEFT_Tools_Demo.ipynb                 # Interactive notebook
├── run_workflow.sh                       # Complete automation script
├── requirements.txt                      # Python dependencies
└── README.md                             # This file
```

---

## Requirements

- Python 3.8+
- InstructLab (latest)
- 16GB+ RAM (model serving)

**Setup**:
```bash
python3 -m venv venv && source venv/bin/activate
pip install instructlab -r requirements.txt
ilab config init
```

**Dependencies**: numpy, pyyaml, evaluate (optional)

---

## Quick Start

```bash
# Terminal 1: Serve baseline model
ilab serve --model-path models/baseline.gguf

# Terminal 2: Generate & evaluate data
ilab data generate --endpoint-url http://localhost:8000/v1
python peft_metrics/data_quality_analyzer.py models/*/generated/*.json report.txt

# Train & convert
ilab model train && ilab model convert

# Serve trained model
ilab serve --model-path models/trained/model.gguf --port 8001

# Terminal 3: Compare models
python peft_evaluation/inference_tester.py \
  --baseline http://localhost:8000/v1 \
  --trained http://localhost:8001/v1 \
  --testset peft_evaluation/example_testset.json
```

---

## Tools

### 1. Data Quality Analyzer ✅

**Path**: [`peft_metrics/data_quality_analyzer.py`](peft_metrics/data_quality_analyzer.py) | **Status**: Complete

**Metrics** (targets):
- `quality_score`: 0-1 (aim 0.70+)
- `duplicate_rate`: % of near-duplicates (<10%)
- `diversity_score`: 0-1 semantic variety (0.50+)
- `avg_rouge_score`: 0.30-0.70 content similarity
- `avg_instruction_length`: 5-15 words
- `avg_output_length`: 30-100 words

**Usage**:
```bash
python peft_metrics/data_quality_analyzer.py <input.json> [output.txt]
```

**Python API**:
```python
from peft_metrics.data_quality_analyzer import DataQualityAnalyzer

analyzer = DataQualityAnalyzer("data.json")
metrics = analyzer.calculate_metrics()
duplicates = analyzer.identify_duplicates(threshold=0.95)
analyzer.generate_report("report.txt")
```

---

### Tool 2: Model Inference Tester 🟢 Complete

Compares baseline and trained models on standardized test cases.

**Location**: [`peft_evaluation/inference_tester.py`](peft_evaluation/inference_tester.py)

**Features:**
- Automated inference testing on both models
- Response quality evaluation (EXCELLENT/GOOD/PARTIAL/POOR)
- Domain-specific accuracy tracking
- Difficulty-based performance analysis
- Side-by-side model comparison
- Performance improvement metrics
- Latency benchmarking

**Test Case Format:**

```json
{
    "question": "When did the 2024 Oscars happen?",
    "expected_keywords": ["March", "2024", "10"],
    "category": "oscars",
    "difficulty": "easy"
}
```

**Response Quality Levels:**

| Level | Criteria |
|-------|----------|
| `EXCELLENT` | Directly answers with all key points |
| `GOOD` | Answers with minor issues |
| `PARTIAL` | Partially correct or incomplete |
| `POOR` | Incorrect or irrelevant |

**Python Usage:**

```python
from peft_evaluation.inference_tester import (
    InferenceTester,
    load_testset_from_file,
    save_comparison_report
)

# Load test cases
test_cases = load_testset_from_file("peft_evaluation/example_testset.json")

# Create tester
tester = InferenceTester(
    model_endpoint="http://localhost:8000/v1",
    timeout=30
)

# Compare models
comparison = tester.compare_models(
    baseline_endpoint="http://localhost:8000/v1",
    baseline_model="gpt-oss:20b",
    trained_endpoint="http://localhost:8001/v1",
    trained_model="llama3:70b",
    test_cases=test_cases
)

# Display results
print(f"Accuracy Improvement: {comparison['improvements']['accuracy_change_percent']:+.1f}%")
print(f"Latency Improvement: {comparison['improvements']['latency_improvement_percent']:+.1f}%")

# Save comparison report
save_comparison_report(comparison, "comparison_results.json")
```

**Command Line Usage:**

```bash
python peft_evaluation/inference_tester.py \
    --baseline http://localhost:8000/v1 \
    --trained http://localhost:8001/v1 \
    --testset peft_evaluation/example_testset.json \
    --output comparison_results.json
```

**Output Metrics:**

```
╔══════════════════════════════════════════════════════────════╗
║              MODEL COMPARISON RESULTS                        ║
╚══════════════════════════════════════════════════════════════╝

📈 ACCURACY
──────────────────────────────────────────────────────────────
  Baseline:  75.2%  (94/125)
  Trained:   82.4%  (103/125)
  Change:    +7.2%  🟢

⚡ LATENCY
──────────────────────────────────────────────────────────────
  Baseline:  245 ms
  Trained:   198 ms
  Improvement: -19.2%

✅ SUCCESS RATE
──────────────────────────────────────────────────────────────
  Baseline:  89.6%
  Trained:   94.4%
```

---

### Tool 3: Data Generation Pipeline 🟡 Work in Progress

Orchestrates end-to-end data generation with quality gates and batch processing.

**Location**: [`peft_pipeline/data_generation_pipeline.py`](peft_pipeline/data_generation_pipeline.py)

**Status**: 🚧 **Under Development** - Core functionality complete, optimization in progress

**Features:**
- Automatic domain discovery in taxonomy
- Domain configuration validation
- Parallel data generation with progress tracking
- Integrated quality gates (blocks low-quality data)
- Aggregated reporting and JSON results
- Detailed execution logging

**Pipeline Steps:**

1. ✅ Discover domains in taxonomy
2. ✅ Validate QNA configurations
3. ✅ Generate synthetic data per domain
4. ✅ Analyze data quality
5. ✅ Apply quality gate (configurable threshold)
6. ✅ Generate summary report

**Configuration:**

```python
from peft_pipeline.data_generation_pipeline import (
    PipelineConfig,
    DataGenerationPipeline,
    run_pipeline
)

config = PipelineConfig(
    taxonomy_path="instructlab/taxonomy",
    output_base_dir="./pipeline_output",
    num_instructions=500,
    rouge_threshold=0.75,
    num_cpus=10,
    model_endpoint="http://localhost:8000/v1",
    quality_gate_threshold=0.7,      # Minimum quality to proceed
    seed_examples_min=3
)

pipeline = DataGenerationPipeline(config)
results = pipeline.run()
```

**Python Usage:**

```python
from peft_pipeline.data_generation_pipeline import run_pipeline

# Run full pipeline
results = run_pipeline(
    taxonomy_path="instructlab/taxonomy",
    output_dir="./pipeline_output",
    num_instructions=1000,
    rouge_threshold=0.75,
    quality_threshold=0.7,
    model_endpoint="http://localhost:8000/v1"
)

# Check results
for result in results:
    print(f"Domain: {result.domain}")
    print(f"Status: {result.status}")
    if result.status == "success":
        metrics = result.quality_metrics
        print(f"Quality: {metrics['quality_score']*100:.1f}%")
        print(f"Samples: {metrics['unique_samples']}/{metrics['total_samples']}")
    elif result.status == "quality_gate_blocked":
        print(f"Blocked: {result.error_message}")
    else:
        print(f"Failed: {result.error_message}")
```

**Command Line Usage:**

```bash
python peft_pipeline/data_generation_pipeline.py \
    instructlab/taxonomy \
    --output ./pipeline_output \
    --num-instructions 1000 \
    --rouge-threshold 0.75 \
    --quality-threshold 0.7 \
    --endpoint http://localhost:8000/v1
```

**Output Files:**
- `pipeline_results.json` - Detailed results per domain
- `pipeline_report.txt` - Human-readable summary
- `*/generated_data.json` - Individual domain generated data

---

## Workflow

**Phase 1 (30-60m)**: Generate data → Analyze quality  
**Phase 2 (1-4h)**: Train adapter → Convert model  
**Phase 3 (15-30m)**: Compare baseline vs trained → Report metrics

**Multi-terminal setup**:
```bash
# T1: Baseline (keep running)
ilab serve --model-path models/baseline.gguf

# T2: Generate & train
python peft_pipeline/data_generation_pipeline.py instructlab/taxonomy --output pipeline_output
ilab model train && ilab model convert
ilab serve --model-path models/trained/model.gguf --port 8001

# T3: Evaluate
python peft_evaluation/inference_tester.py --baseline http://localhost:8000/v1 --trained http://localhost:8001/v1 --testset peft_evaluation/example_testset.json
```



---

## Metrics

| Metric | Range | Target | Interpretation |
|--------|-------|--------|----------------|
| **quality_score** | 0-1 | 0.70+ | Overall data quality; 0.85+ is production-ready |
| **duplicate_rate** | % | <10% | Data diversity; >30% indicates too many duplicates |
| **diversity_score** | 0-1 | 0.50+ | Semantic variety; 0.7+ = high variety |
| **accuracy_change** | % | +5% to +10% | Model improvement; <0% = degradation |
| **success_rate** | % | 85%+ | % of correct responses; 95%+ = excellent |
| **latency_improvement** | % | >0% | Negative = faster responses |

**Quality gates**: Default quality_score threshold is 0.7 (tunable)

--- 

## Troubleshooting

| Problem | Solution |
|---------|----------|
| **Endpoint connection failed** | Verify model is running: `ilab serve --model-path model.gguf` on correct port (default 8000) |
| **Low quality scores** | Increase seed examples (5+), improve diversity, lower rouge_threshold (0.60 vs 0.75) |
| **High duplicate rate** | Lower rouge_threshold, add diverse seed examples, manually review seeds |
| **Inference tester timeout** | Increase `--timeout` parameter, ensure models on different ports, check network |
| **Training loss not decreasing** | Check data quality >0.7, increase iterations, review seed example quality/diversity |



---
## References

- **InstructLab Documentation**: https://github.com/instructlab/instructlab
- **Parameter-Efficient Fine-Tuning**: https://arxiv.org/abs/2106.04560
- **PEFT Library**: https://github.com/huggingface/peft
- **HuggingFace Evaluate**: https://github.com/huggingface/evaluate

---