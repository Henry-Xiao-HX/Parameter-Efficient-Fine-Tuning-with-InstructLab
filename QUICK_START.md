"""
Quick Start Guide for PEFT Tools

This guide shows how to use the three new tools:
1. Data Quality Analyzer
2. Data Generation Pipeline
3. Inference Tester
"""

# ============================================================================
# 1. DATA QUALITY ANALYZER
# ============================================================================
# Analyze the quality of generated synthetic data

from peft_metrics.data_quality_analyzer import analyze_generated_data

# Analyze a generated data file
metrics = analyze_generated_data(
    data_path="models/2024_oscars/generated/generated_*.json",
    output_report="quality_report.txt"
)

# Print specific metrics
print(f"Quality Score: {metrics.quality_score}")
print(f"Duplicate Rate: {metrics.duplicate_rate:.1%}")
print(f"Diversity: {metrics.diversity_score}")


# ============================================================================
# 2. AUTOMATED DATA GENERATION PIPELINE
# ============================================================================
# Run end-to-end data generation with quality gates

from peft_pipeline.data_generation_pipeline import run_pipeline, PipelineConfig

# Run full pipeline with parameters
results = run_pipeline(
    taxonomy_path="instructlab/taxonomy",
    output_dir="./pipeline_results",
    num_instructions=1000,
    rouge_threshold=0.75,
    quality_threshold=0.7,  # Minimum quality score to proceed
    model_endpoint="http://localhost:8000/v1"
)

# Check results for each domain
for result in results:
    print(f"Domain: {result.domain}")
    print(f"Status: {result.status}")
    if result.status == "success":
        print(f"Quality: {result.quality_metrics['quality_score']}")
        print(f"Data File: {result.data_file}")


# ============================================================================
# 3. MODEL INFERENCE TESTER
# ============================================================================
# Compare baseline and trained models

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
    baseline_endpoint="http://localhost:8000/v1",  # Original model
    trained_endpoint="http://localhost:8001/v1",   # Trained model
    test_cases=test_cases
)

# Save comparison report
save_comparison_report(comparison, "comparison_results.json")

print(f"Accuracy Improvement: {comparison['improvements']['accuracy_change_percent']:+.1f}%")


# ============================================================================
# COMPLETE WORKFLOW EXAMPLE
# ============================================================================

def complete_fine_tuning_workflow():
    """
    Complete workflow from data generation to evaluation
    """
    import subprocess
    
    print("🚀 Starting Complete Fine-Tuning Workflow\n")
    
    # Step 1: Generate data with pipeline
    print("1️⃣  Generating synthetic data...")
    results = run_pipeline(
        taxonomy_path="instructlab/taxonomy",
        output_dir="./pipeline_output",
        num_instructions=500,
        quality_threshold=0.7
    )
    
    successful_domains = [r for r in results if r.status == "success"]
    if not successful_domains:
        print("❌ No domains passed quality gate. Aborting.")
        return
    
    print(f"✅ {len(successful_domains)} domains ready for training\n")
    
    # Step 2: Train model
    print("2️⃣  Training model...")
    cmd = ["ilab", "model", "train"]
    subprocess.run(cmd)
    
    print("✅ Training complete\n")
    
    # Step 3: Convert model
    print("3️⃣  Converting model...")
    cmd = ["ilab", "model", "convert"]
    subprocess.run(cmd)
    
    print("✅ Model converted\n")
    
    # Step 4: Evaluate trained model
    print("4️⃣  Evaluating trained model...")
    
    test_cases = load_testset_from_file("peft_evaluation/example_testset.json")
    tester = InferenceTester()
    
    # Serve baseline
    baseline_proc = subprocess.Popen(
        ["ilab", "serve", "--model-path", "models/baseline-model.gguf"],
        stdout=subprocess.DEVNULL
    )
    
    # Serve trained
    trained_proc = subprocess.Popen(
        ["ilab", "serve", "--model-path", "models/trained-model.gguf", "--port", "8001"],
        stdout=subprocess.DEVNULL
    )
    
    import time
    time.sleep(5)  # Wait for servers to start
    
    try:
        comparison = tester.compare_models(
            baseline_endpoint="http://localhost:8000/v1",
            trained_endpoint="http://localhost:8001/v1",
            test_cases=test_cases
        )
        
        save_comparison_report(comparison, "final_comparison.json")
        
        print("\n✅ Evaluation complete!")
        print(f"Accuracy Improvement: {comparison['improvements']['accuracy_change_percent']:+.1f}%")
        
    finally:
        baseline_proc.terminate()
        trained_proc.terminate()


if __name__ == "__main__":
    # Uncomment to run complete workflow
    # complete_fine_tuning_workflow()
    
    # Or use tools individually:
    print("Import these modules in your scripts:")
    print("  from peft_metrics.data_quality_analyzer import DataQualityAnalyzer")
    print("  from peft_pipeline.data_generation_pipeline import run_pipeline")
    print("  from peft_evaluation.inference_tester import InferenceTester")
