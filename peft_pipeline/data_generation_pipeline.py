"""
Automated Data Generation Pipeline for PEFT

Orchestrates the entire workflow:
- Batch QNA processing
- Parallel data generation with progress tracking
- Quality gates before training
- Results aggregation and reporting
"""

import os
import json
import subprocess
import time
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
import shutil
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from peft_metrics.data_quality_analyzer import DataQualityAnalyzer, QualityMetrics


@dataclass
class PipelineConfig:
    """Configuration for pipeline execution"""
    taxonomy_path: str
    output_base_dir: str
    num_instructions: int = 500
    rouge_threshold: float = 0.75
    num_cpus: int = 10
    model_endpoint: str = "http://localhost:8000/v1"
    quality_gate_threshold: float = 0.7  # Minimum quality score to proceed
    seed_examples_min: int = 3  # Minimum seed examples per domain
    
    def to_dict(self):
        return asdict(self)


@dataclass
class PipelineResult:
    """Result of pipeline execution"""
    domain: str
    status: str  # "success", "failed", "quality_gate_blocked"
    timestamp: str
    data_file: Optional[str] = None
    quality_metrics: Optional[Dict] = None
    error_message: Optional[str] = None
    execution_time: float = 0.0


class DataGenerationPipeline:
    """Orchestrates end-to-end data generation"""

    def __init__(self, config: PipelineConfig):
        """
        Initialize pipeline with configuration
        
        Args:
            config: PipelineConfig object
        """
        self.config = config
        self.output_dir = Path(config.output_base_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.results: List[PipelineResult] = []

    def discover_domains(self) -> List[str]:
        """
        Discover available domains/skills in taxonomy
        
        Returns:
            List of domain paths
        """
        taxonomy_path = Path(self.config.taxonomy_path)
        domains = []
        
        # Look for qna.yaml files in taxonomy
        if taxonomy_path.exists():
            for qna_file in taxonomy_path.rglob("qna.yaml"):
                domain_path = qna_file.parent
                domains.append(str(domain_path))
        
        return sorted(domains)

    def validate_domain_config(self, domain_path: str) -> bool:
        """
        Validate domain has valid qna.yaml with enough seed examples
        
        Args:
            domain_path: Path to domain directory
            
        Returns:
            True if valid, False otherwise
        """
        qna_file = Path(domain_path) / "qna.yaml"
        
        if not qna_file.exists():
            return False
        
        # Parse YAML to check seed examples
        try:
            import yaml
            with open(qna_file, 'r') as f:
                content = yaml.safe_load(f)
                seed_examples = content.get('seed_examples', [])
                return len(seed_examples) >= self.config.seed_examples_min
        except:
            return False

    def generate_data_for_domain(self, domain_path: str) -> Optional[str]:
        """
        Generate synthetic data for a single domain
        
        Args:
            domain_path: Path to domain directory
            
        Returns:
            Path to generated data file, or None on failure
        """
        domain_name = Path(domain_path).name
        print(f"\n📊 Generating data for domain: {domain_name}")
        
        try:
            cmd = [
                "ilab", "data", "generate",
                "--endpoint-url", self.config.model_endpoint,
                "--num-instructions", str(self.config.num_instructions),
                "--rouge-threshold", str(self.config.rouge_threshold),
                "--num-cpus", str(self.config.num_cpus),
            ]
            
            print(f"  Running: {' '.join(cmd)}")
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=domain_path)
            
            if result.returncode != 0:
                print(f"  ✗ Error: {result.stderr}")
                return None
            
            # Find generated data file
            generated_files = list(Path(domain_path).glob("generated/*.json"))
            if generated_files:
                return str(generated_files[0])
            
            return None
            
        except Exception as e:
            print(f"  ✗ Exception: {e}")
            return None

    def evaluate_data_quality(self, data_file: str) -> Optional[QualityMetrics]:
        """
        Evaluate quality of generated data
        
        Args:
            data_file: Path to generated data file
            
        Returns:
            QualityMetrics object or None
        """
        try:
            analyzer = DataQualityAnalyzer(data_file)
            metrics = analyzer.calculate_metrics()
            return metrics
        except Exception as e:
            print(f"  ✗ Quality analysis failed: {e}")
            return None

    def process_domain(self, domain_path: str) -> PipelineResult:
        """
        Process entire pipeline for a single domain
        
        Args:
            domain_path: Path to domain directory
            
        Returns:
            PipelineResult with status and metrics
        """
        domain_name = Path(domain_path).name
        start_time = time.time()
        
        print(f"\n{'='*60}")
        print(f"Processing Domain: {domain_name}")
        print(f"{'='*60}")
        
        result = PipelineResult(
            domain=domain_name,
            status="failed",
            timestamp=datetime.now().isoformat()
        )
        
        try:
            # Step 1: Validate domain configuration
            print(f"\n1️⃣  Validating domain configuration...")
            if not self.validate_domain_config(domain_path):
                result.error_message = "Insufficient seed examples or invalid qna.yaml"
                result.status = "failed"
                print(f"  ✗ {result.error_message}")
                return result
            print(f"  ✓ Domain configuration valid")
            
            # Step 2: Generate synthetic data
            print(f"\n2️⃣  Generating synthetic data...")
            data_file = self.generate_data_for_domain(domain_path)
            
            if not data_file:
                result.error_message = "Data generation failed"
                result.status = "failed"
                print(f"  ✗ {result.error_message}")
                return result
            
            print(f"  ✓ Data generated: {data_file}")
            result.data_file = data_file
            
            # Step 3: Analyze data quality
            print(f"\n3️⃣  Analyzing data quality...")
            metrics = self.evaluate_data_quality(data_file)
            
            if not metrics:
                result.error_message = "Quality analysis failed"
                result.status = "failed"
                return result
            
            result.quality_metrics = asdict(metrics)
            print(f"  Quality Score: {metrics.quality_score * 100:.1f}%")
            print(f"  Unique Samples: {metrics.unique_samples}/{metrics.total_samples}")
            print(f"  Diversity: {metrics.diversity_score * 100:.1f}%")
            
            # Step 4: Quality gate
            print(f"\n4️⃣  Quality Gate Check (threshold: {self.config.quality_gate_threshold})")
            if metrics.quality_score < self.config.quality_gate_threshold:
                result.status = "quality_gate_blocked"
                result.error_message = (
                    f"Quality score {metrics.quality_score:.2f} below threshold "
                    f"{self.config.quality_gate_threshold}"
                )
                print(f"  ⚠ {result.error_message}")
                print(f"  → Recommendation: Review seed examples and regenerate")
                return result
            
            print(f"  ✓ Quality gate passed")
            
            result.status = "success"
            result.execution_time = time.time() - start_time
            
            print(f"\n✅ Domain processed successfully ({result.execution_time:.1f}s)")
            
        except Exception as e:
            result.status = "failed"
            result.error_message = str(e)
            print(f"  ✗ Unexpected error: {e}")
        
        return result

    def run(self) -> List[PipelineResult]:
        """
        Execute full pipeline for all discovered domains
        
        Returns:
            List of PipelineResult objects
        """
        print("\n🚀 Starting Data Generation Pipeline")
        print(f"{'='*60}")
        print(f"Taxonomy Path: {self.config.taxonomy_path}")
        print(f"Output Directory: {self.output_dir}")
        print(f"{'='*60}\n")
        
        # Discover domains
        domains = self.discover_domains()
        print(f"📍 Found {len(domains)} domain(s)\n")
        
        if not domains:
            print("⚠ No domains found in taxonomy")
            return []
        
        # Process each domain
        for domain_path in domains:
            result = self.process_domain(domain_path)
            self.results.append(result)
        
        # Generate summary report
        self._generate_summary_report()
        
        return self.results

    def _generate_summary_report(self):
        """Generate and save pipeline summary report"""
        successful = [r for r in self.results if r.status == "success"]
        blocked = [r for r in self.results if r.status == "quality_gate_blocked"]
        failed = [r for r in self.results if r.status == "failed"]
        
        report = f"""
╔══════════════════════════════════════════════════════════════╗
║         PIPELINE EXECUTION SUMMARY REPORT                    ║
╚══════════════════════════════════════════════════════════════╝

⏰ Timestamp: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

📊 OVERALL RESULTS
{'─'*60}
  Total Domains Processed: {len(self.results)}
  ✅ Successful:           {len(successful)}
  ⚠ Blocked by Quality:    {len(blocked)}
  ✗ Failed:                {len(failed)}

"""
        
        if successful:
            report += f"\n✅ SUCCESSFUL DOMAINS ({len(successful)}):\n"
            report += f"{'─'*60}\n"
            for result in successful:
                metrics = result.quality_metrics
                report += (
                    f"  • {result.domain}\n"
                    f"    - Quality: {metrics['quality_score']*100:.1f}%\n"
                    f"    - Samples: {metrics['unique_samples']}/{metrics['total_samples']}\n"
                    f"    - File: {result.data_file}\n"
                    f"    - Time: {result.execution_time:.1f}s\n\n"
                )
        
        if blocked:
            report += f"\n⚠ BLOCKED BY QUALITY GATE ({len(blocked)}):\n"
            report += f"{'─'*60}\n"
            for result in blocked:
                metrics = result.quality_metrics
                report += (
                    f"  • {result.domain}\n"
                    f"    - Quality Score: {metrics['quality_score']*100:.1f}%\n"
                    f"    - Reason: {result.error_message}\n\n"
                )
        
        if failed:
            report += f"\n✗ FAILED ({len(failed)}):\n"
            report += f"{'─'*60}\n"
            for result in failed:
                report += f"  • {result.domain}\n    - Error: {result.error_message}\n\n"
        
        report += f"\n💾 Full results saved to: {self._save_results()}\n"
        report += f"{'='*60}\n"
        
        print(report)
        
        # Save report
        report_file = self.output_dir / "pipeline_report.txt"
        with open(report_file, 'w') as f:
            f.write(report)

    def _save_results(self) -> str:
        """Save detailed results as JSON"""
        results_file = self.output_dir / "pipeline_results.json"
        
        results_data = {
            "timestamp": datetime.now().isoformat(),
            "config": self.config.to_dict(),
            "results": [asdict(r) for r in self.results]
        }
        
        with open(results_file, 'w') as f:
            json.dump(results_data, f, indent=2)
        
        return str(results_file)


def run_pipeline(
    taxonomy_path: str,
    output_dir: str = "./pipeline_output",
    num_instructions: int = 500,
    rouge_threshold: float = 0.75,
    quality_threshold: float = 0.7,
    model_endpoint: str = "http://localhost:8000/v1"
) -> List[PipelineResult]:
    """
    Convenience function to run the pipeline
    
    Args:
        taxonomy_path: Path to InstructLab taxonomy
        output_dir: Directory for outputs
        num_instructions: Number of instructions to generate
        rouge_threshold: ROUGE threshold for generation
        quality_threshold: Minimum quality score
        model_endpoint: Model API endpoint
        
    Returns:
        List of PipelineResults
    """
    config = PipelineConfig(
        taxonomy_path=taxonomy_path,
        output_base_dir=output_dir,
        num_instructions=num_instructions,
        rouge_threshold=rouge_threshold,
        quality_gate_threshold=quality_threshold,
        model_endpoint=model_endpoint
    )
    
    pipeline = DataGenerationPipeline(config)
    return pipeline.run()


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Automated Data Generation Pipeline")
    parser.add_argument("taxonomy", help="Path to InstructLab taxonomy")
    parser.add_argument("--output", default="./pipeline_output", help="Output directory")
    parser.add_argument("--num-instructions", type=int, default=500, help="Number of instructions")
    parser.add_argument("--rouge-threshold", type=float, default=0.75, help="ROUGE threshold")
    parser.add_argument("--quality-threshold", type=float, default=0.7, help="Quality gate threshold")
    parser.add_argument("--endpoint", default="http://localhost:8000/v1", help="Model endpoint")
    
    args = parser.parse_args()
    
    run_pipeline(
        taxonomy_path=args.taxonomy,
        output_dir=args.output,
        num_instructions=args.num_instructions,
        rouge_threshold=args.rouge_threshold,
        quality_threshold=args.quality_threshold,
        model_endpoint=args.endpoint
    )
