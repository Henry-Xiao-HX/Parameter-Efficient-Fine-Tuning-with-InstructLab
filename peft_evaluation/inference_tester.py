"""
Model Inference & Testing Framework for PEFT

Compares trained vs. baseline models on:
- Question-answering accuracy
- Domain retention metrics
- Capability degradation analysis
- Performance benchmarking
"""

import json
import time
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, asdict
import subprocess
from enum import Enum


class ResponseQuality(Enum):
    """Quality rating for model responses"""
    EXCELLENT = "excellent"  # Directly answers question accurately
    GOOD = "good"             # Answers with minor issues
    PARTIAL = "partial"       # Partially correct/incomplete
    POOR = "poor"             # Incorrect or irrelevant


@dataclass
class TestCase:
    """Single test case for model evaluation"""
    question: str
    expected_keywords: List[str]  # Keywords that should appear in response
    category: str                  # Domain/category for this test
    difficulty: str = "medium"    # easy, medium, hard


@dataclass
class InferenceResult:
    """Result of single model inference"""
    question: str
    response: str
    latency_ms: float
    tokens_generated: int


@dataclass
class ModelEvaluationMetrics:
    """Metrics for model evaluation"""
    model_name: str
    total_tests: int
    correct_responses: int
    partial_responses: int
    incorrect_responses: int
    timeout_responses: int
    accuracy: float                # Correct/Total
    success_rate: float             # (Correct + Partial)/Total
    avg_latency_ms: float
    domains_accuracy: Dict[str, float]  # Accuracy per domain
    difficulty_accuracy: Dict[str, float]  # Accuracy by difficulty


class InferenceTester:
    """Tests and evaluates trained models"""

    def __init__(self, model_endpoint: str = "http://localhost:8000/v1", timeout: int = 30):
        """
        Initialize tester with model endpoint
        
        Args:
            model_endpoint: URL of model API endpoint
            timeout: Request timeout in seconds
        """
        self.model_endpoint = model_endpoint
        self.timeout = timeout
        self.results: List[InferenceResult] = []

    def run_inference(self, question: str) -> Optional[InferenceResult]:
        """
        Run single inference query against model
        
        Args:
            question: Question to ask model
            
        Returns:
            InferenceResult or None on timeout
        """
        try:
            start_time = time.time()
            
            # Use curl or requests to query model
            import subprocess
            
            cmd = [
                "curl", "-s",
                "-X", "POST",
                f"{self.model_endpoint}/chat/completions",
                "-H", "Content-Type: application/json",
                "-d", json.dumps({
                    "model": "instructlab-model",
                    "messages": [{"role": "user", "content": question}],
                    "temperature": 0.7,
                    "max_tokens": 200
                })
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=self.timeout)
            
            if result.returncode != 0:
                return None
            
            latency = time.time() - start_time
            response_data = json.loads(result.stdout)
            
            response_text = response_data.get("choices", [{}])[0].get("message", {}).get("content", "")
            tokens = len(response_text.split())
            
            return InferenceResult(
                question=question,
                response=response_text,
                latency_ms=latency * 1000,
                tokens_generated=tokens
            )
            
        except subprocess.TimeoutExpired:
            return None
        except Exception as e:
            print(f"Error during inference: {e}")
            return None

    def _evaluate_response(
        self, 
        response: str, 
        expected_keywords: List[str]
    ) -> ResponseQuality:
        """
        Evaluate quality of model response
        
        Args:
            response: Model's response
            expected_keywords: Keywords that should appear
            
        Returns:
            ResponseQuality rating
        """
        if not response:
            return ResponseQuality.POOR
        
        response_lower = response.lower()
        
        # Count keyword matches
        keyword_matches = 0
        for keyword in expected_keywords:
            if keyword.lower() in response_lower:
                keyword_matches += 1
        
        match_ratio = keyword_matches / len(expected_keywords) if expected_keywords else 0
        
        # Determine quality based on keyword matches and length
        response_length = len(response.split())
        
        if match_ratio >= 0.8 and response_length > 20:
            return ResponseQuality.EXCELLENT
        elif match_ratio >= 0.6 and response_length > 15:
            return ResponseQuality.GOOD
        elif match_ratio >= 0.4 and response_length > 10:
            return ResponseQuality.PARTIAL
        else:
            return ResponseQuality.POOR

    def evaluate_on_testset(
        self,
        test_cases: List[TestCase]
    ) -> ModelEvaluationMetrics:
        """
        Evaluate model on set of test cases
        
        Args:
            test_cases: List of TestCase objects
            
        Returns:
            ModelEvaluationMetrics object
        """
        results = {
            "excellent": 0,
            "good": 0,
            "partial": 0,
            "poor": 0,
            "timeout": 0
        }
        
        domain_results = {}
        difficulty_results = {}
        latencies = []
        
        print(f"\n🧪 Running inference tests ({len(test_cases)} cases)...")
        print(f"{'─'*60}")
        
        for i, test_case in enumerate(test_cases, 1):
            # Run inference
            inference = self.run_inference(test_case.question)
            
            if not inference:
                results["timeout"] += 1
                quality = ResponseQuality.POOR
                latency = self.timeout * 1000
            else:
                latencies.append(inference.latency_ms)
                quality = self._evaluate_response(
                    inference.response,
                    test_case.expected_keywords
                )
                latency = inference.latency_ms
                results[quality.value] += 1
            
            # Track by domain
            if test_case.category not in domain_results:
                domain_results[test_case.category] = {"total": 0, "correct": 0}
            
            domain_results[test_case.category]["total"] += 1
            if quality in [ResponseQuality.EXCELLENT, ResponseQuality.GOOD]:
                domain_results[test_case.category]["correct"] += 1
            
            # Track by difficulty
            if test_case.difficulty not in difficulty_results:
                difficulty_results[test_case.difficulty] = {"total": 0, "correct": 0}
            
            difficulty_results[test_case.difficulty]["total"] += 1
            if quality in [ResponseQuality.EXCELLENT, ResponseQuality.GOOD]:
                difficulty_results[test_case.difficulty]["correct"] += 1
            
            # Print progress
            status_icon = {
                ResponseQuality.EXCELLENT: "✓",
                ResponseQuality.GOOD: "✓",
                ResponseQuality.PARTIAL: "~",
                ResponseQuality.POOR: "✗"
            }.get(quality, "?")
            
            print(f"  [{i:2d}] {status_icon} {quality.value:9s} ({latency:6.0f}ms) {test_case.category}")
        
        # Calculate metrics
        total = len(test_cases)
        correct = results["excellent"] + results["good"]
        success = correct + results["partial"]
        
        avg_latency = sum(latencies) / len(latencies) if latencies else 0
        
        # Calculate per-domain accuracy
        domains_accuracy = {
            domain: round(data["correct"] / data["total"], 3)
            for domain, data in domain_results.items()
        }
        
        # Calculate per-difficulty accuracy
        difficulty_accuracy = {
            diff: round(data["correct"] / data["total"], 3)
            for diff, data in difficulty_results.items()
        }
        
        metrics = ModelEvaluationMetrics(
            model_name="Unknown",
            total_tests=total,
            correct_responses=correct,
            partial_responses=results["partial"],
            incorrect_responses=results["poor"],
            timeout_responses=results["timeout"],
            accuracy=round(correct / total, 3) if total > 0 else 0,
            success_rate=round(success / total, 3) if total > 0 else 0,
            avg_latency_ms=round(avg_latency, 2),
            domains_accuracy=domains_accuracy,
            difficulty_accuracy=difficulty_accuracy
        )
        
        return metrics

    def compare_models(
        self,
        baseline_endpoint: str,
        trained_endpoint: str,
        test_cases: List[TestCase]
    ) -> Dict:
        """
        Compare baseline model with trained model
        
        Args:
            baseline_endpoint: URL of baseline model
            trained_endpoint: URL of trained model
            test_cases: Test cases to evaluate on
            
        Returns:
            Dictionary with comparison results
        """
        print("\n" + "="*60)
        print("📊 MODEL COMPARISON: BASELINE vs TRAINED")
        print("="*60)
        
        # Evaluate baseline
        print("\n🔵 Evaluating BASELINE model...")
        self.model_endpoint = baseline_endpoint
        baseline_metrics = self.evaluate_on_testset(test_cases)
        baseline_metrics.model_name = "Baseline"
        
        # Evaluate trained
        print("\n🟢 Evaluating TRAINED model...")
        self.model_endpoint = trained_endpoint
        trained_metrics = self.evaluate_on_testset(test_cases)
        trained_metrics.model_name = "Trained"
        
        # Calculate improvements
        accuracy_improvement = (
            (trained_metrics.accuracy - baseline_metrics.accuracy) / 
            baseline_metrics.accuracy * 100
            if baseline_metrics.accuracy > 0 else 0
        )
        
        latency_improvement = (
            (baseline_metrics.avg_latency_ms - trained_metrics.avg_latency_ms) / 
            baseline_metrics.avg_latency_ms * 100
            if baseline_metrics.avg_latency_ms > 0 else 0
        )
        
        comparison = {
            "baseline": asdict(baseline_metrics),
            "trained": asdict(trained_metrics),
            "improvements": {
                "accuracy_change_percent": round(accuracy_improvement, 2),
                "latency_improvement_percent": round(latency_improvement, 2),
                "additional_correct_responses": (
                    trained_metrics.correct_responses - baseline_metrics.correct_responses
                )
            }
        }
        
        self._print_comparison(baseline_metrics, trained_metrics, comparison["improvements"])
        
        return comparison

    def _print_comparison(
        self,
        baseline: ModelEvaluationMetrics,
        trained: ModelEvaluationMetrics,
        improvements: Dict
    ):
        """Print formatted comparison results"""
        report = f"""
╔══════════════════════════════════════════════════════════════╗
║              MODEL COMPARISON RESULTS                        ║
╚══════════════════════════════════════════════════════════════╝

📈 ACCURACY
{'─'*60}
  Baseline:  {baseline.accuracy*100:5.1f}%  ({baseline.correct_responses}/{baseline.total_tests})
  Trained:   {trained.accuracy*100:5.1f}%  ({trained.correct_responses}/{trained.total_tests})
  Change:    {improvements['accuracy_change_percent']:+.1f}%  {'🟢' if improvements['accuracy_change_percent'] > 0 else '🔴'}

⚡ LATENCY
{'─'*60}
  Baseline:  {baseline.avg_latency_ms:6.0f} ms
  Trained:   {trained.avg_latency_ms:6.0f} ms
  Improvement: {improvements['latency_improvement_percent']:+.1f}%

✅ SUCCESS RATE
{'─'*60}
  Baseline:  {baseline.success_rate*100:5.1f}%
  Trained:   {trained.success_rate*100:5.1f}%

📊 BREAKDOWN
{'─'*60}
  Baseline Errors:  {baseline.incorrect_responses + baseline.timeout_responses} incorrect + {baseline.timeout_responses} timeouts
  Trained Errors:   {trained.incorrect_responses + trained.timeout_responses} incorrect + {trained.timeout_responses} timeouts

🎯 ACCURACY BY DOMAIN
{'─'*60}
"""
        
        all_domains = set(baseline.domains_accuracy.keys()) | set(trained.domains_accuracy.keys())
        for domain in sorted(all_domains):
            baseline_acc = baseline.domains_accuracy.get(domain, 0) * 100
            trained_acc = trained.domains_accuracy.get(domain, 0) * 100
            change = trained_acc - baseline_acc
            icon = "🟢" if change > 0 else "🔴" if change < 0 else "⚪"
            report += f"  {domain:20s}: {baseline_acc:5.1f}% → {trained_acc:5.1f}% {icon}\n"
        
        report += f"\n{'='*60}\n"
        print(report)


def load_testset_from_file(filepath: str) -> List[TestCase]:
    """
    Load test cases from JSON file
    
    Expected format:
    [
        {
            "question": "...",
            "expected_keywords": ["key1", "key2"],
            "category": "domain_name",
            "difficulty": "easy|medium|hard"
        }
    ]
    """
    with open(filepath, 'r') as f:
        data = json.load(f)
    
    return [TestCase(**item) for item in data]


def save_comparison_report(comparison: Dict, output_file: str):
    """Save comparison results to file"""
    with open(output_file, 'w') as f:
        json.dump(comparison, f, indent=2)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Model Inference Tester")
    parser.add_argument("--baseline", required=True, help="Baseline model endpoint")
    parser.add_argument("--trained", required=True, help="Trained model endpoint")
    parser.add_argument("--testset", required=True, help="Path to test cases JSON file")
    parser.add_argument("--output", help="Output file for comparison report")
    parser.add_argument("--timeout", type=int, default=30, help="Request timeout in seconds")
    
    args = parser.parse_args()
    
    # Load test cases
    print("Loading test cases...")
    test_cases = load_testset_from_file(args.testset)
    print(f"Loaded {len(test_cases)} test cases")
    
    # Run comparison
    tester = InferenceTester(timeout=args.timeout)
    comparison = tester.compare_models(args.baseline, args.trained, test_cases)
    
    # Save results
    if args.output:
        save_comparison_report(comparison, args.output)
        print(f"\n💾 Results saved to: {args.output}")
