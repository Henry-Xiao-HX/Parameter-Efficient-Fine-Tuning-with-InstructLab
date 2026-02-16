"""
Data Quality Metrics & Analysis Tool for PEFT

Evaluates generated synthetic data for:
- Answer diversity and uniqueness
- Response length distribution
- Quality scoring based on semantic similarity
- Duplicate detection
- ROUGE score analysis
"""

import json
import os
from pathlib import Path
from collections import Counter
from typing import List, Dict, Tuple
import numpy as np
from dataclasses import dataclass, asdict


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
    diversity_score: float  # 0-1, based on semantic variety
    quality_score: float    # 0-1, overall quality metric


class DataQualityAnalyzer:
    """Analyzes quality of synthetic training data"""

    def __init__(self, data_file_path: str):
        """
        Initialize analyzer with generated data file
        
        Args:
            data_file_path: Path to generated*.json or *.jsonl file
        """
        self.data_file_path = Path(data_file_path)
        self.data = self._load_data()

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

        # ROUGE-based metrics
        rouge_scores = self._calculate_rouge_scores()
        avg_rouge = np.mean(rouge_scores) if rouge_scores else 0
        min_rouge = np.min(rouge_scores) if rouge_scores else 0
        max_rouge = np.max(rouge_scores) if rouge_scores else 0

        # Diversity score
        diversity_score = self._calculate_diversity_score()

        # Overall quality score
        quality_score = self._calculate_overall_quality(
            duplicate_rate, avg_rouge, diversity_score
        )

        return QualityMetrics(
            total_samples=total_samples,
            unique_samples=unique_samples,
            duplicate_rate=duplicate_rate,
            avg_instruction_length=round(avg_instruction_length, 2),
            avg_output_length=round(avg_output_length, 2),
            length_std_dev=round(length_std_dev, 2),
            avg_rouge_score=round(avg_rouge, 2),
            min_rouge_score=round(min_rouge, 2),
            max_rouge_score=round(max_rouge, 2),
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

    def _calculate_rouge_scores(self) -> List[float]:
        """
        Simple ROUGE-L implementation for diversity/content overlap
        Returns list of scores (0-1) for each sample's uniqueness
        """
        scores = []
        outputs = [str(d.get('output', '')) for d in self.data]
        
        for i, current_output in enumerate(outputs):
            if not current_output:
                scores.append(1.0)
                continue
            
            # Compare with other outputs (simple word overlap)
            current_words = set(current_output.lower().split())
            max_overlap = 0
            
            for j, other_output in enumerate(outputs):
                if i != j:
                    other_words = set(other_output.lower().split())
                    if current_words and other_words:
                        overlap = len(current_words & other_words) / len(current_words | other_words)
                        max_overlap = max(max_overlap, overlap)
            
            uniqueness = 1.0 - max_overlap
            scores.append(uniqueness)
        
        return scores

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
        diversity_score: float
    ) -> float:
        """
        Calculate overall quality score (0-1)
        Weighted combination of metrics
        """
        # Lower duplicate rate is better
        uniqueness_score = 1 - duplicate_rate
        
        # Higher diversity is better
        # Higher average ROUGE (similarity to existing) should penalize, but not too much
        diversity_weight = diversity_score
        
        # Quality = 40% uniqueness + 30% diversity + 30% consistency
        quality = (
            uniqueness_score * 0.4 +
            diversity_weight * 0.3 +
            (1 - avg_rouge) * 0.3
        )
        
        return min(quality, 1.0)

    def identify_duplicates(self, threshold: float = 0.95) -> List[Tuple[int, int]]:
        """
        Identify duplicate or near-duplicate samples
        
        Args:
            threshold: Similarity threshold (0-1)
            
        Returns:
            List of tuples (index1, index2) of similar pairs
        """
        duplicates = []
        
        for i in range(len(self.data)):
            for j in range(i + 1, len(self.data)):
                inst_i = str(self.data[i].get('instruction', '')).lower()
                inst_j = str(self.data[j].get('instruction', '')).lower()
                
                # Simple similarity: word overlap ratio
                words_i = set(inst_i.split())
                words_j = set(inst_j.split())
                
                if words_i and words_j:
                    similarity = len(words_i & words_j) / len(words_i | words_j)
                    
                    if similarity >= threshold:
                        duplicates.append((i, j, round(similarity, 3)))
        
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

🔄 DIVERSITY & SIMILARITY
─────────────────────────────────────────────────────────────
  Diversity Score:            {metrics.diversity_score * 100:.1f}%
  Avg ROUGE Score:            {metrics.avg_rouge_score:.3f}
  ROUGE Range:                [{metrics.min_rouge_score:.3f}, {metrics.max_rouge_score:.3f}]

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
