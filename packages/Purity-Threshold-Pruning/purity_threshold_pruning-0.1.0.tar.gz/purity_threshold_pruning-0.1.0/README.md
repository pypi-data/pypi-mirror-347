# Purity-Threshold-Pruning

## About
Purity Threshold Pruning is a bagging‑based tree‑ensemble pruning algorithm for scikit‑learn’s RandomForestClassifier that minimizes model complexity under a user‑specified accuracy‑loss tolerance.

The main advantages are:
 - Explicitly consider node purity (i.e., class distribution), preventing the pruning of low purity nodes that may cause catastrophic accuracy degradation.
 - Iteratively search for the minimum purity threshold that satisfies the tolerance, resulting in the smallest possible model that satisfies the desired performance.
 - Systematical pruning prevents the model from overgrowing or being over-pruned.

## Installation

### From PyPI (recommended)
```
pip install purity-threshold-pruning
```

### From GitHub
```
git clone https://github.com/Datou0718/Purity-Threshold-Pruning
cd Purity-Threshold-Pruning
pip install .
```

## Quick Start

```
from PurityThresholdPruning import PurityThresholdPruning
from sklearn.ensemble import RandomForestClassifier

# train a Random Forest
rf = RandomForestClassifier(...)
rf.fit(X_train, y_train)

# Pruned the model with 5% tolerable accuracy loss
tolerance = 0.05 
rf = PurityThresholdPruning(rf, tolerance, X_train, y_train)
```

## API
```PurityThresholdPruning(forest, tolerance, X_train, y_train)```
- forest: a fitted `RandomForestClassifier` with `oob_score=True`.
- tolerance: Maximum tolerable accuracy drop in OOB estimation (e.g., `0.05` for 5%).
- X, y: Training data (np.ndarray) used to compute OOB score.
Returns the `RandomForestClassifier` pruned with the minimum purity threshold.