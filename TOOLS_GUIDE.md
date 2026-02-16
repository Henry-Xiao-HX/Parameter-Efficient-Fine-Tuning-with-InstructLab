# PEFT Tools Implementation Guide

This document describes the three new tools implemented for improving Parameter Efficient Fine-Tuning workflows.

## 📦 Tools Overview

### 1. Data Quality Analyzer (`peft_metrics/data_quality_analyzer.py`)

Evaluates the quality of synthetic training data before model training.

**Features:**
- Duplicate detection and reporting
- Semantic diversity scoring (vocabulary & n-gram analysis)
- ROUGE-based similarity metrics
- Length distribution analysis
- Comprehensive quality score (0-1)
- Actionable recommendations

**Key Metrics:**
- `quality_score`: Overall quality (0-1)
- `duplicate_rate`: Percentage of duplicate/near-duplicate samples
- `diversity_score`: Semantic variety (0-1)
- `avg_rouge_score`: Average content similarity

**Usage:**
```python
from peft_metrics.data_quality_analyzer import analyze_generated_data

metrics = analyze_generated_data(
    data_path="models/2024_oscars/generated/generated_*.json",
    output_report="quality_report.txt"
)

print(f"Quality: {metrics.quality_score * 100:.1f}%")
```

**Command Line:**
```bash
python peft_metrics/data_quality_analyzer.py path/to/generated_data.json output_report.txt
```

---

### 2. Automated Data Generation Pipeline (`peft_pipeline/data_generation_pipeline.py`)

Orchestrates end-to-end data generation with quality gates and batch processing.

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
from peft_pipeline.data_generation_pipeline import PipelineConfig, DataGenerationPipeline

config = PipelineConfig(
    taxonomy_path="instructlab/taxonomy",
    output_base_dir="./pipeline_output",
    num_instructions=500,
    rouge_threshold=0.75,
    num_cpus=10,
    model_endpoint="http://localhost:8000/v1",
    quality_gate_threshold=0.7,  # Minimum quality to proceed
    seed_examples_min=3
)

pipeline = DataGenerationPipeline(config)
results = pipeline.run()
```

**Command Line:**
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
- `pipeline_results.json`: Detailed results per domain
- `pipeline_report.txt`: Human-readable summary
- Individual domain generated data files

---

### 3. Model Inference Tester (`peft_evaluation/inference_tester.py`)

Compares baseline and trained models on standardized test cases.

**Features:**
- Automated inference testing
- Response quality evaluation
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
- `EXCELLENT`: Directly answers with all key points
- `GOOD`: Answers with minor issues
- `PARTIAL`: Partially correct/incomplete
- `POOR`: Incorrect or irrelevant

**Usage:**
```python
from peft_evaluation.inference_tester import InferenceTester, load_testset_from_file

test_cases = load_testset_from_file("peft_evaluation/example_testset.json")

tester = InferenceTester(model_endpoint="http://localhost:8000/v1")

comparison = tester.compare_models(
    baseline_endpoint="http://localhost:8000/v1",
    trained_endpoint="http://localhost:8001/v1",
    test_cases=test_cases
)

print(f"Accuracy Improvement: {comparison['improvements']['accuracy_change_percent']:+.1f}%")
```

**Command Line:**
```bash
python peft_evaluation/inference_tester.py \
    --baseline http://localhost:8000/v1 \
    --trained http://localhost:8001/v1 \
    --testset peft_evaluation/example_testset.json \
    --output comparison_results.json
```

**Output Metrics:**
- Overall accuracy and success rates
- Per-domain accuracy
- Per-difficulty performance
- Latency improvements
- Response distribution

---

## 🔄 Integration into Workflow

### Recommended Workflow:

```bash
# 1. Serve baseline model
ilab serve --model-path models/baseline.gguf

# 2. Generate synthetic data with quality gates
python peft_pipeline/data_generation_pipeline.py \
    instructlab/taxonomy \
    --output pipeline_output \
    --quality-threshold 0.7

# 3. Train model (using data from pipeline_output)
ilab model train

# 4. Convert trained model
ilab model convert

# 5. Serve trained model (in another terminal)
ilab serve --model-path models/trained/model.gguf --port 8001

# 6. Compare models
python peft_evaluation/inference_tester.py \
    --baseline http://localhost:8000/v1 \
    --trained http://localhost:8001/v1 \
    --testset peft_evaluation/example_testset.json \
    --output results.json
```

---

## 📊 Understanding the Metrics

### Data Quality Analyzer
- **Quality Score**: Composite metric combining:
  - Uniqueness (40%): 1 - duplicate_rate
  - Diversity (30%): Semantic variety score
  - Consistency (30%): 1 - avg_rouge_overlap

### Data Generation Pipeline
- **Status**: success, failed, quality_gate_blocked
- **Quality Metrics**: All metrics from Data Quality Analyzer
- **Execution Time**: How long domain took to process

### Inference Tester
- **Accuracy**: Correct / Total (percentage)
- **Success Rate**: (Correct + Partial) / Total
- **Domain Accuracy**: Per-category performance
- **Latency**: Average response time in milliseconds

---

## 🎯 Quality Thresholds

Recommended thresholds for different use cases:

| Use Case | Quality Threshold | Notes |
|----------|-------------------|-------|
| Strict Quality | 0.85+ | Production deployment |
| Standard | 0.70-0.84 | General training |
| Experimental | 0.50-0.69 | Research/testing |
| Permissive | <0.50 | Quick iteration |

---

## 🚀 Example Scripts

### Complete Fine-Tuning Pipeline
See `QUICK_START.md` for full working examples.

### Custom Quality Analysis
```python
from peft_metrics.data_quality_analyzer import DataQualityAnalyzer

analyzer = DataQualityAnalyzer("path/to/data.json")

# Get comprehensive metrics
metrics = analyzer.calculate_metrics()

# Find duplicates
duplicates = analyzer.identify_duplicates(threshold=0.95)

# Get statistics
stats = analyzer.get_sample_statistics()

# Generate report
report = analyzer.generate_report("report.txt")
```

### Per-Domain Analysis
```python
from peft_pipeline.data_generation_pipeline import DataGenerationPipeline, PipelineConfig

config = PipelineConfig(
    taxonomy_path="instructlab/taxonomy",
    output_base_dir="./results",
    quality_gate_threshold=0.7
)

pipeline = DataGenerationPipeline(config)
results = pipeline.run()

# Analyze results
for result in results:
    if result.status == "success":
        print(f"{result.domain}: {result.quality_metrics['quality_score']}")
    elif result.status == "quality_gate_blocked":
        print(f"{result.domain}: Blocked - {result.error_message}")
```

---

## ⚙️ Dependencies

All tools use only standard Python libraries:
- `json`, `pathlib`, `subprocess`, `time`, `dataclasses`
- `numpy` (for statistical analysis)
- YAML parsing (if needed for QNA validation)

Optional:
- `pyyaml`: For domain validation

---

## 📝 File Structure

```
repository/
├── peft_metrics/
│   └── data_quality_analyzer.py
├── peft_pipeline/
│   └── data_generation_pipeline.py
├── peft_evaluation/
│   ├── inference_tester.py
│   └── example_testset.json
├── QUICK_START.md
└── TOOLS_GUIDE.md (this file)
```

---

## 🔧 Tips & Tricks

1. **Batch Processing**: Run pipeline for multiple domains at once
2. **Quality Gates**: Reject data below threshold before training
3. **Test Coverage**: Include easy/medium/hard questions
4. **Domain Isolation**: Measure accuracy per domain separately
5. **Iterative Improvement**: Re-run pipeline after seed example refinement

---

## 📞 Troubleshooting

**Pipeline fails on model endpoint**
- Ensure model is running: `ilab serve --model-path model.gguf`
- Check endpoint URL matches (default: `http://localhost:8000/v1`)

**Low quality scores**
- Increase seed examples in qna.yaml (aim for 5+)
- Improve seed example quality and diversity
- Increase `num_instructions` for more training data

**Inference tester timeout**
- Increase `--timeout` parameter
- Ensure both models are running on different ports
- Check network connectivity between client and server

**Duplicate data detected**
- Lower `rouge_threshold` in pipeline (e.g., 0.60 vs 0.75)
- Add more diverse seed examples
- Regenerate data with different model

---

## 📈 Next Steps

1. Start with small dataset (3-5 seed examples)
2. Run quality analyzer on generated data
3. Use pipeline to automate multi-domain processing
4. Compare models before/after training
5. Iterate on seed examples based on results

Recommended reading: See `QUICK_START.md` for runnable examples.
