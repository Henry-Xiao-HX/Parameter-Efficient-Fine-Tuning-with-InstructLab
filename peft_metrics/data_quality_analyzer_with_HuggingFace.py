"""
Data Quality Metrics & Analysis Tool for PEFT

Evaluates generated synthetic data using HuggingFace Evaluate library for:
- Answer diversity and uniqueness
- Response length distribution
- Quality scoring based on ROUGE and semantic similarity
- Duplicate detection
- BLEU score analysis
"""

import json
import os
from pathlib import Path
from collections import Counter
from typing import List, Dict, Tuple
import numpy as np
from dataclasses import dataclass, asdict

import evaluate
from evaluate import load


@dataclass
class QualityMetrics:
    """Container for quality metrics"""
    total_samples: int
    unique_samples: int
    duplicate_rate: float
    avg_instruction_length: float
    avg_output_length: float
    length_std_dev: float
    avg_rouge_score: float
    min_rouge_score: float
    max_rouge_score: float
    avg_bleu_score: float
    diversity_score: float  # 0-1, based on semantic variety
    quality_score: float    # 0-1, overall quality metric


class DataQualityAnalyzer:
    """Analyzes quality of synthetic training data using HF Evaluate"""

    def __init__(self, data_file_path: str):
        """
        Initialize analyzer with generated data file
        
        Args:
            data_file_path: Path to generated*.json or *.jsonl file
        """
        self.data_file_path = Path(data_file_path)
        self.data = self._load_data()
        
        # Load HF Evaluate metrics
        self.rouge_metric = load('rouge')
        self.bleu_metric = load('bleu')

    def _load_data(self) -> List[Dict]:
        """Load JSON or JSONL data"""
        data = []
        
        if self.data_file_path.suffix == '.jsonl':
            with open(self.data_file_path, 'r') as f:
                for line in f:
                    if line.strip():
                        data.append(json.loads(line))
        else:
            with open(self.data_file_path, 'r') as f:
                data = json.load(f)
        
        return data

    def calculate_metrics(self) -> QualityMetrics:
        """Calculate all quality metrics"""
        if not self.data:
            raise ValueError("No data loaded")

        # Basic counts
        total_samples = len(self.data)
        unique_samples = self._count_unique_samples()
        duplicate_rate = 1 - (unique_samples / total_samples) if total_samples > 0 else 0

        # Length statistics
        instruction_lengths = [len(str(d.get('instruction', '')).split()) for d in self.data]
        output_lengths = [len(str(d.get('output', '')).split()) for d in self.data]
        
        avg_instruction_length = np.mean(instruction_lengths) if instruction_lengths else 0
        avg_output_length = np.mean(output_lengths) if output_lengths else 0
        length_std_dev = np.std(output_lengths) if output_lengths else 0

        # ROUGE-based metrics using HF Evaluate
        rouge_scores = self._calculate_rouge_scores_hf()
        avg_rouge = np.mean(rouge_scores) if rouge_scores else 0
        min_rouge = np.min(rouge_scores) if rouge_scores else 0
        max_rouge = np.max(rouge_scores) if rouge_scores else 0

        # BLEU score using HF Evaluate
        avg_bleu = self._calculate_bleu_score_hf()

        # Diversity score
        diversity_score = self._calculate_diversity_score()

        # Overall quality score
        quality_score = self._calculate_overall_quality(
            duplicate_rate, avg_rouge, diversity_score, avg_bleu
        )

        return QualityMetrics(
            total_samples=total_samples,
            unique_samples=unique_samples,
            duplicate_rate=duplicate_rate,
            avg_instruction_length=round(avg_instruction_length, 2),
            avg_output_length=round(avg_output_length, 2),
            length_std_dev=round(length_std_dev, 2),
            avg_rouge_score=round(avg_rouge, 4),
            min_rouge_score=round(min_rouge, 4),
            max_rouge_score=round(max_rouge, 4),
            avg_bleu_score=round(avg_bleu, 4),
            diversity_score=round(diversity_score, 2),
            quality_score=round(quality_score, 2)
        )

    def _count_unique_samples(self) -> int:
        """Count unique instruction-output pairs"""
        unique_pairs = set()
        for item in self.data:
            pair = (
                item.get('instruction', ''),
                item.get('output', '')
            )
            unique_pairs.add(pair)
        return len(unique_pairs)

    def _calculate_rouge_scores_hf(self) -> List[float]:
        """
        Calculate ROUGE-L scores using HuggingFace Evaluate library
        Measures semantic similarity between outputs
        """
        scores = []
        outputs = [str(d.get('output', '')) for d in self.data]
        
        for i, current_output in enumerate(outputs):
            if not current_output:
                scores.append(1.0)
                continue
            
            # Compare current output against all others
            other_outputs = [outputs[j] for j in range(len(outputs)) if i != j]
            
            if not other_outputs:
                scores.append(1.0)
                continue
            
            try:
                # Calculate ROUGE-L score
                results = self.rouge_metric.compute(
                    predictions=[current_output] * len(other_outputs),
                    references=other_outputs,
                    rouge_types=['rougeL']
                )
                
                # Use average rougeL as overlap metric
                avg_overlap = results['rougeL']
                uniqueness = 1.0 - avg_overlap
                scores.append(uniqueness)
            except Exception as e:
                print(f"Warning: ROUGE calculation failed for sample {i}: {e}")
                scores.append(0.5)
        
        return scores

    def _calculate_bleu_score_hf(self) -> float:
        """
        Calculate average BLEU score using HuggingFace Evaluate library
        Measures translation quality / output consistency
        """
        outputs = [str(d.get('output', '')) for d in self.data]
        
        if len(outputs) < 2:
            return 0.0
        
        try:
            # Use first half as predictions, second half as references
            mid = len(outputs) // 2
            predictions = outputs[:mid]
            references = [[ref] for ref in outputs[mid:mid + len(predictions)]]
            
            results = self.bleu_metric.compute(
                predictions=predictions,
                references=references
            )
            
            return results.get('bleu', 0.0)
        except Exception as e:
            print(f"Warning: BLEU calculation failed: {e}")
            return 0.0

    def _calculate_diversity_score(self) -> float:
        """
        Calculate semantic diversity based on:
        - Vocabulary variety
        - Unique n-grams
        - Topic distribution
        """
        all_words = []
        all_bigrams = []
        
        for item in self.data:
            output = str(item.get('output', '')).lower().split()
            all_words.extend(output)
            
            # Extract bigrams
            for i in range(len(output) - 1):
                all_bigrams.append((output[i], output[i + 1]))
        
        if not all_words:
            return 0.0
        
        # Vocabulary diversity (unique words / total words)
        unique_words = len(set(all_words))
        vocab_diversity = min(unique_words / len(all_words), 1.0)
        
        # Bigram diversity
        unique_bigrams = len(set(all_bigrams))
        bigram_diversity = min(unique_bigrams / len(all_bigrams), 1.0) if all_bigrams else 0
        
        # Combined diversity score
        diversity = (vocab_diversity * 0.6 + bigram_diversity * 0.4)
        return diversity

    def _calculate_overall_quality(
        self, 
        duplicate_rate: float, 
        avg_rouge: float,
        diversity_score: float,
        avg_bleu: float
    ) -> float:
        """
        Calculate overall quality score (0-1)
        Weighted combination of metrics
        """
        # Lower duplicate rate is better
        uniqueness_score = 1 - duplicate_rate
        
        # Higher diversity is better
        diversity_weight = diversity_score
        
        # Normalize BLEU score (typically 0-1)
        bleu_weight = min(avg_bleu, 1.0)
        
        # Quality = 35% uniqueness + 30% diversity + 20% consistency + 15% BLEU
        quality = (
            uniqueness_score * 0.35 +
            diversity_weight * 0.30 +
            (1 - avg_rouge) * 0.20 +
            bleu_weight * 0.15
        )
        
        return min(quality, 1.0)

    def identify_duplicates(self, threshold: float = 0.95) -> List[Tuple[int, int, float]]:
        """
        Identify duplicate or near-duplicate samples using HF Evaluate
        
        Args:
            threshold: Similarity threshold (0-1)
            
        Returns:
            List of tuples (index1, index2, similarity) of similar pairs
        """
        duplicates = []
        instructions = [str(d.get('instruction', '')).lower() for d in self.data]
        
        for i in range(len(self.data)):
            for j in range(i + 1, len(self.data)):
                inst_i = instructions[i]
                inst_j = instructions[j]
                
                if not inst_i or not inst_j:
                    continue
                
                try:
                    # Use ROUGE to compare instructions
                    results = self.rouge_metric.compute(
                        predictions=[inst_i],
                        references=[inst_j],
                        rouge_types=['rougeL']
                    )
                    
                    similarity = results['rougeL']
                    
                    if similarity >= threshold:
                        duplicates.append((i, j, round(similarity, 3)))
                except Exception as e:
                    print(f"Warning: Duplicate detection failed for samples {i}, {j}: {e}")
        
        return duplicates

    def get_sample_statistics(self) -> Dict:
        """Get distribution statistics of samples"""
        instruction_lengths = [len(str(d.get('instruction', '')).split()) for d in self.data]
        output_lengths = [len(str(d.get('output', '')).split()) for d in self.data]
        
        return {
            "instruction_length": {
                "min": int(np.min(instruction_lengths)) if instruction_lengths else 0,
                "max": int(np.max(instruction_lengths)) if instruction_lengths else 0,
                "mean": round(np.mean(instruction_lengths), 2) if instruction_lengths else 0,
                "median": round(np.median(instruction_lengths), 2) if instruction_lengths else 0,
            },
            "output_length": {
                "min": int(np.min(output_lengths)) if output_lengths else 0,
                "max": int(np.max(output_lengths)) if output_lengths else 0,
                "mean": round(np.mean(output_lengths), 2) if output_lengths else 0,
                "median": round(np.median(output_lengths), 2) if output_lengths else 0,
            }
        }

    def generate_report(self, output_file: str = None) -> str:
        """
        Generate comprehensive quality report
        
        Args:
            output_file: Optional file to save report
            
        Returns:
            Formatted report string
        """
        metrics = self.calculate_metrics()
        stats = self.get_sample_statistics()
        duplicates = self.identify_duplicates()
        
        report = f"""
╔══════════════════════════════════════════════════════════════╗
║           DATA QUALITY ANALYSIS REPORT                       ║
║              (HF Evaluate-based Analysis)                    ║
╚══════════════════════════════════════════════════════════════╝

📊 DATASET OVERVIEW
─────────────────────────────────────────────────────────────
  Total Samples:              {metrics.total_samples}
  Unique Samples:             {metrics.unique_samples}
  Duplicate Rate:             {metrics.duplicate_rate:.1%}
  Potential Duplicates Found: {len(duplicates)}

📏 LENGTH ANALYSIS
─────────────────────────────────────────────────────────────
  Instruction Length (words):
    • Average: {metrics.avg_instruction_length}
    • Min: {stats['instruction_length']['min']}
    • Max: {stats['instruction_length']['max']}
    • Median: {stats['instruction_length']['median']}
  
  Output Length (words):
    • Average: {metrics.avg_output_length}
    • Min: {stats['output_length']['min']}
    • Max: {stats['output_length']['max']}
    • Median: {stats['output_length']['median']}
    • Std Dev: {metrics.length_std_dev}

🔄 DIVERSITY & SIMILARITY METRICS
─────────────────────────────────────────────────────────────
  Diversity Score:            {metrics.diversity_score * 100:.1f}%
  Avg ROUGE-L Score:          {metrics.avg_rouge_score:.4f}
  ROUGE Range:                [{metrics.min_rouge_score:.4f}, {metrics.max_rouge_score:.4f}]
  Avg BLEU Score:             {metrics.avg_bleu_score:.4f}

⭐ OVERALL QUALITY
─────────────────────────────────────────────────────────────
  Quality Score:              {metrics.quality_score * 100:.1f}%
  
  Rating: {"✓ Excellent" if metrics.quality_score > 0.85 
           else "✓ Good" if metrics.quality_score > 0.7
           else "⚠ Fair" if metrics.quality_score > 0.5
           else "✗ Poor"}

📋 RECOMMENDATIONS
─────────────────────────────────────────────────────────────
"""
        
        recommendations = []
        if metrics.duplicate_rate > 0.1:
            recommendations.append("  • High duplicate rate detected. Consider increasing ROUGE threshold")
        if metrics.diversity_score < 0.5:
            recommendations.append("  • Low diversity. Add more varied seed examples to qna.yaml")
        if metrics.avg_output_length < 20:
            recommendations.append("  • Short responses. Consider prompting for more detailed answers")
        if metrics.avg_bleu_score < 0.3:
            recommendations.append("  • Low BLEU score indicates low consistency. Review output quality")
        if metrics.quality_score < 0.7:
            recommendations.append("  • Consider regenerating data with better seed examples")
        
        if recommendations:
            report += "\n".join(recommendations)
        else:
            report += "  ✓ Data quality looks good!"
        
        report += "\n\n╚══════════════════════════════════════════════════════════════╝\n"
        
        if output_file:
            with open(output_file, 'w') as f:
                f.write(report)
        
        return report


def analyze_generated_data(data_path: str, output_report: str = None) -> QualityMetrics:
    """
    Convenience function to analyze generated data
    
    Args:
        data_path: Path to generated data file
        output_report: Optional file to save report
        
    Returns:
        QualityMetrics object
    """
    analyzer = DataQualityAnalyzer(data_path)
    metrics = analyzer.calculate_metrics()
    report = analyzer.generate_report(output_report)
    print(report)
    return metrics


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        data_file = sys.argv[1]
        output_file = sys.argv[2] if len(sys.argv) > 2 else None
        analyze_generated_data(data_file, output_file)
    else:
        print("Usage: python data_quality_analyzer.py <data_file> [output_report]")
