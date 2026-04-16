---
type: synthesized
aliases: ["random-forest-mechanism", "random-forest-vs-bagging"]
tags: ["random-forest", "ensemble-methods", "bagging", "decorrelation", "overfitting", "feature-subsets", "bootstrap"]
relationships:
  - target: bagging
    type: extends
  - target: bias-variance-tradeoff
    type: relates-to
  - target: automatic-feature-selection
    type: relates-to
---

# Random Forest: Double Decorrelation as the Core Mechanism

## The Core Insight

Random forests are often described loosely as "many decision trees averaged together," but this undersells the precise mechanism that makes them work. The key is **double decorrelation**: randomness is injected along two independent axes simultaneously, and it is this combination—not mere averaging—that gives random forests their characteristic resistance to overfitting.

## Two Axes of Randomness

### Axis 1 — Rows: Bootstrap Sampling
Each tree in the forest is trained on a **bootstrap sample**: a dataset of the same size as the original, drawn with replacement. On average, about 63% of the original rows appear in any given bootstrap sample; the rest are "out-of-bag" (OOB) and can be used for free validation. This row-level randomness is shared with plain bagging.

### Axis 2 — Columns: Random Feature Subsets at Each Split
At **every node** of every tree, only a random subset of features is considered as candidates for the split. A common default is √p features for classification and p/3 for regression, where p is the total number of features. This column-level randomness is what distinguishes random forests from plain bagging.

## Why Double Decorrelation Matters

In plain bagging, trees are still correlated because they all have access to the same strong predictors. If one feature dominates, most trees will split on it near the root, producing similar structures. Averaging correlated trees reduces variance less than averaging independent trees.

By restricting the feature candidates at each split, random forests **break the dominance of strong predictors**. Trees are forced to find good splits using different subsets of features, producing structurally diverse trees. The ensemble average then benefits from near-independence, dramatically reducing variance without increasing bias proportionally.

Formally, if trees have pairwise correlation ρ and individual variance σ², the ensemble variance is:


ρ·σ² + (1−ρ)·σ²/n


Reducing ρ (decorrelating trees) shrinks the irreducible first term, which averaging alone cannot touch.

## Contrast with Related Methods

| Method | Row randomness | Column randomness | Tree correlation |
|---|---|---|---|
| Single decision tree | None | None | N/A |
| Bagging | Bootstrap samples | Full feature set | High (strong predictors dominate) |
| **Random Forest** | **Bootstrap samples** | **Random subset per split** | **Low** |
| Boosting | Reweighted/resampled | Full (usually) | Sequential, not decorrelated |

Boosting reduces bias by sequentially correcting errors; random forests reduce variance by decorrelating parallel trees. They attack different parts of the bias-variance tradeoff.

## Practical Implications

- **Overfitting resistance**: Because variance is suppressed through decorrelation, random forests are robust even with deep, unpruned trees. Individual trees overfit; the ensemble does not.
- **OOB error**: The unused ~37% of rows per tree provides a built-in validation estimate without a separate hold-out set.
- **Feature importance**: The column-level randomness also enables reliable permutation-based feature importance scores, since every feature gets a chance to contribute across different trees.
- **Hyperparameter sensitivity**: The number of features per split (often called `max_features`) is the most important tuning parameter—it directly controls the decorrelation level.

## Summary Framing

> Random forests do not merely average trees; they engineer diversity among trees by withholding information at every split. The double decorrelation—across rows via bootstrapping and across columns via random feature subsets—is the mechanism. Averaging is just the aggregation step that harvests the benefit of that diversity.