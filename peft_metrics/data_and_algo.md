# Rouge-L and Longest Common Subsequence

```python
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
```

User: @workspace /explain Write an explanation for the active selection as paragraphs of text.

```python
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
```



Workspace: # Understanding `_calculate_rouge_scores()`

## Purpose and Overview

This method implements a simplified ROUGE-L scoring mechanism to measure the uniqueness of each generated output in your dataset. Rather than computing true ROUGE scores, it calculates how much each output overlaps with others—higher uniqueness means less semantic similarity to any other sample. The result is a list of scores between 0 and 1 for each sample, where 1.0 represents completely unique content and 0.0 represents content that's nearly identical to some other sample.

## Step-by-Step Breakdown

The method begins by extracting all output strings from `self.data`, converting them to strings and handling missing values gracefully. It then iterates through each output with an index, checking for empty strings first. If an output is empty, it's assigned a perfect uniqueness score of 1.0 and skipped—the assumption being that empty outputs can't duplicate anything meaningful.

For non-empty outputs, the algorithm converts the current output to lowercase and splits it into individual words, storing them in a set called `current_words`. This set representation is key because it enables efficient intersection and union operations later. The variable `max_overlap` is initialized to zero and will track the highest similarity found between the current output and any other output.

## The Comparison Loop

The nested loop compares the current output against all other outputs in the dataset. For each comparison, it extracts words from the other output the same way and checks if both sets are non-empty. The overlap is calculated using the **Jaccard similarity coefficient**:

$$\text{overlap} = \frac{|\text{current\_words} \cap \text{other\_words}|}{|\text{current\_words} \cup \text{other\_words}|}$$

This formula divides the count of common words by the count of total unique words across both sets. The result ranges from 0 (no words in common) to 1 (identical word sets). The `max_overlap` variable is updated to keep track of the highest similarity score found.

## Inverting to Uniqueness

Once all comparisons are complete, the uniqueness score is calculated as `1.0 - max_overlap`. This inversion transforms the most similar match into a uniqueness penalty. If an output shares 60% of its words with another output, its uniqueness score becomes 0.4, reflecting that it's not very unique.

## Gotchas and Considerations

**Watch out for the empty set check**: The condition `if current_words and other_words` prevents division by zero, but it also means comparisons skip empty outputs entirely. This is intentional but worth noting—empty outputs won't affect uniqueness scores even if they appear multiple times.

**Word-level granularity**: This approach treats "running" and "runner" as different words because it only splits on whitespace. For more sophisticated duplicate detection, consider adding stemming or lemmatization.

**Performance consideration**: This is an $O(n^2)$ algorithm where $n$ is the number of samples. For datasets with thousands of outputs, this could become slow. Caching or using approximate nearest-neighbor search might help at scale.

# Vocabulary and Bigram Diversity Calculation

## _calculate_diversity_score()

### Purpose and Data Structure

This method measures semantic diversity across the entire dataset by analyzing vocabulary richness and n-gram patterns. It returns a single score between 0 and 1, where 1.0 represents maximum diversity and 0.0 represents monotonous, repetitive content. The method uses two main data structures:

- **`all_words`**: A flat list accumulating every word from every output
- **`all_bigrams`**: A list of tuples, each containing sequential word pairs

These structures enable efficient computation of unique word and bigram counts across the entire dataset.

### Vocabulary Diversity Calculation

The algorithm first iterates through all data items, extracting the output field, converting it to lowercase, and splitting it into individual words. Every word is appended to `all_words`. Simultaneously, the algorithm constructs bigrams (two-word sequences) by sliding a window across consecutive words and appending tuples like `("the", "model")` to `all_bigrams`.

The vocabulary diversity metric is calculated as:

$$\text{vocab\_diversity} = \min\left(\frac{|\text{unique\_words}|}{|\text{total\_words}|}, 1.0\right)$$

This ratio represents the lexical variety: a dataset where every word is unique has a score approaching 1.0, while a dataset using the same 10 words repeatedly drops toward 0.0. The `min()` ensures the score never exceeds 1.0.

### Bigram Diversity and Weighting

Similarly, bigram diversity measures phrase-level variety:

$$\text{bigram\_diversity} = \min\left(\frac{|\text{unique\_bigrams}|}{|\text{total\_bigrams}|}, 1.0\right)$$

If no bigrams exist (single-word outputs), this scores 0. The final diversity score combines both metrics with empirically chosen weights:

$$\text{diversity} = (\text{vocab\_diversity} \times 0.6) + (\text{bigram\_diversity} \times 0.4)$$

The 60-40 split prioritizes vocabulary variety while rewarding structural diversity in word ordering.

---

# Quality Scoring With Weighted Metrics

## _calculate_overall_quality()

### Purpose and Design Philosophy

This method produces a single summary quality score (0-1) by combining four independent metrics with carefully tuned weights. It accepts four parameters representing different quality dimensions and returns a composite score that balances multiple concerns.

### Four Quality Dimensions

**1. Uniqueness Score**: Derived from duplicate rate with the formula:

$$\text{uniqueness\_score} = 1 - \text{duplicate\_rate}$$

A dataset with 10% duplicates achieves a uniqueness score of 0.9. This directly penalizes repetitive content.

**2. Diversity Weight**: Passed directly as the `diversity_score` parameter (already computed by `_calculate_diversity_score()`). No transformation is needed since it's already on the 0-1 scale.

**3. Consistency Metric**: Calculated as `1 - avg_rouge`, inverting the average ROUGE score. High ROUGE overlap (semantic similarity) is transformed into a consistency penalty. When outputs are very similar to each other (high ROUGE), this metric scores low.

**4. BLEU Component**: Normalized with `min(avg_bleu, 1.0)` to ensure it stays within bounds. BLEU measures translation quality and response consistency. Scores naturally range 0-1 but may occasionally exceed this, hence the clamping.

### Weighted Aggregation

The final quality score is the weighted sum:

$$\text{quality} = (0.35 \times \text{uniqueness}) + (0.30 \times \text{diversity}) + (0.20 \times \text{consistency}) + (0.15 \times \text{BLEU})$$

The weights reflect importance hierarchy:
- **35%**: Uniqueness—most critical; duplicates are immediately problematic
- **30%**: Diversity—nearly as important; varied vocabulary helps model generalization
- **20%**: Consistency—important but secondary; ROUGE penalizes overly-similar outputs
- **15%**: BLEU—useful signal but less central; indicates fluency without being paramount

The result is clamped with `min(quality, 1.0)` to guarantee a score ≤ 1.0, though the weighted sum of four values each < 1.0 should naturally stay below 1.0.

### Interpretation

- **Quality > 0.85**: Excellent data suitable for immediate fine-tuning
- **Quality 0.7-0.85**: Good data; minor improvements recommended
- **Quality 0.5-0.7**: Fair data; significant improvements suggested
- **Quality < 0.5**: Poor data; regeneration recommended

---

# Duplicate Detection With Similarity Thresholding

## identify_duplicates()

### Purpose and Return Structure

This method discovers near-duplicate samples by comparing instructions across the dataset. It returns a list of tuples: `[(index1, index2, similarity), ...]` where each tuple represents a detected duplicate pair and its similarity score. The `threshold` parameter (default 0.95) controls sensitivity: higher values only flag near-identical pairs, while lower values flag loosely related instructions.

### Algorithm Overview

The method uses a nested loop with $O(n^2)$ time complexity, comparing every pair of instructions exactly once:

```
for i in range(0, n):
    for j in range(i+1, n):
        compare(instruction[i], instruction[j])
```

By starting the inner loop at `i+1`, duplicates are found only once (avoiding symmetric pairs like `(0,1)` and `(1,0)`).

### Similarity Computation via HF Evaluate

Each instruction pair is compared using the HuggingFace Evaluate library's ROUGE metric:

```python
results = self.rouge_metric.compute(
    predictions=[inst_i],
    references=[inst_j],
    rouge_types=['rougeL']
)
similarity = results['rougeL']
```

ROUGE-L measures the longest common subsequence between two texts, making it robust to word reordering. A ROUGE-L score of 0.95 indicates 95% sequence similarity.

### Threshold Filtering

Only pairs meeting `similarity >= threshold` are added to the duplicates list:

$$\text{add to results if: } \text{ROUGE}_L(i, j) \geq \text{threshold}$$

This binary decision ensures only sufficiently similar pairs are flagged, reducing false positives.

### Data Preparation

Before comparison, all instructions are converted to lowercase strings, normalizing capitalization:

```python
instructions = [str(d.get('instruction', '')).lower() for d in self.data]
```

Empty instructions are skipped with `if not inst_i or not inst_j`, preventing meaningless comparisons.

### Error Handling

Each ROUGE computation is wrapped in a try-except block, logging warnings if specific pairs fail (e.g., due to encoding issues) without crashing the entire analysis.

---

# Distribution Statistics Aggregation

## get_sample_statistics()

### Purpose and Data Structure

This method computes distributional statistics on sample lengths (instructions and outputs), returning a nested dictionary with min, max, mean, and median values for each dimension. The structure is:

```python
{
  "instruction_length": {
    "min": int,
    "max": int,
    "mean": float,
    "median": float
  },
  "output_length": {
    "min": int,
    "max": int,
    "mean": float,
    "median": float
  }
}
```

### Length Extraction

The method first extracts lengths by splitting each field into words:

```python
instruction_lengths = [
    len(str(d.get('instruction', '')).split())
    for d in self.data
]
```

This list comprehension:
1. Retrieves the instruction field (defaulting to empty string if missing)
2. Converts to string type (defensive programming for non-string data)
3. Splits on whitespace (`.split()`)
4. Counts resulting tokens with `len()`

The same process repeats for outputs, creating `output_lengths`.

### Statistical Computations

Four statistics are computed using NumPy:

- **Minimum**: `np.min()` returns the smallest length
- **Maximum**: `np.max()` returns the largest length  
- **Mean**: `np.mean()` computes the arithmetic average
- **Median**: `np.median()` finds the middle value (50th percentile)

Each is wrapped in a conditional check `if lengths` to avoid errors on empty datasets.

### Data Type Handling

- **Min/Max**: Converted to `int` using `int(np.min(...))` for clean JSON serialization
- **Mean/Median**: Rounded to 2 decimal places with `round(..., 2)` for readability

### Use Cases

This dictionary enables:
- **Quality assessment**: Median output length indicates typical response size
- **Balance checking**: Compare instruction vs. output lengths to ensure data isn't instruction-heavy
- **Outlier detection**: Large ranges between min and max suggest outliers
- **Reporting**: Display in human-readable tables showing dataset characteristics

**Example interpretation**: 
- Instruction mean of 8.5 words suggests clear, concise queries
- Output median of 45 words with max 120 indicates varied but controlled response lengths


