import gc
import copy
import numpy as np
from sklearn.ensemble import RandomForestClassifier

def GeneratePurity(forest: RandomForestClassifier) -> list:
    """
    Given a RandomForestClassifier, compute the purity of each node.
    """
    pruity = []
    for estimator in forest.estimators_:
        counts = estimator.tree_.value.squeeze(axis=1)
        maj = np.argmax(counts, axis=1)
        pur = counts[np.arange(counts.shape[0]), maj] / counts.sum(axis=1)
        pruity.append(list(np.round(pur, 2)))
        
    return pruity


def PurityThresholdPruning(forest: RandomForestClassifier, tolerance: float, X_train: np.ndarray, y_train: np.ndarray) -> RandomForestClassifier:
    """
    Prune the RandomForestClassifier with tolerance and purity threshold pruning.
    """
    purity = GeneratePurity(forest)
    min_threshold = MinThresholdSearch(forest, purity, tolerance, X_train, y_train)
    pruned_forest = PruneModel(forest, purity, min_threshold, X_train, y_train)
    # print(f"Out-of-bag score before pruning: {forest.oob_score_}")
    # print(f"Out-of-bag score after pruning: {pruned_forest.oob_score_}")
    
    return pruned_forest


def MinThresholdSearch(forest: RandomForestClassifier, purity: list, tolerance: float, X_train: np.ndarray, y_train: np.ndarray) -> float:
    """
    Search for the minimum threshold that satisfies the tolerance condition.
    """
    lower_bound, upper_bound, threshold, min_threshold = 0, 1, 1, 1
    unpruned_oob_score, pruned_oob_score = forest.oob_score_, 0
    
    while lower_bound <= upper_bound:
        threshold = round((lower_bound + upper_bound) / 2, 2)        
        pruned_forest = PruneModel(forest, purity, threshold, X_train, y_train)
        pruned_oob_score = pruned_forest.oob_score_
        if pruned_oob_score >= unpruned_oob_score - tolerance:
            min_threshold = threshold
            upper_bound = threshold - 0.01
        else:
            lower_bound = threshold + 0.01
        
        FreeModel(pruned_forest)
            
    return min_threshold


def PruneModel(forest: RandomForestClassifier, purity: list, threshold: float, X_train: np.ndarray, y_train: np.ndarray) -> RandomForestClassifier:
    """
    Prune the RandomForestClassifier based on the purity of each node.
    """
    # hard copy the forest to avoid modifying the original
    pruned_forest = copy.deepcopy(forest)
    
    for i, estimator in enumerate(pruned_forest.estimators_):
        for j, pur in enumerate(purity[i]):
            if pur > threshold:
                estimator.tree_.children_left[j] = -1
                estimator.tree_.children_right[j] = -1

    pruned_forest.oob_score_ = ComputeOOBScore(pruned_forest, X_train, y_train)
    
    return pruned_forest


def ComputeOOBScore(forest: RandomForestClassifier, X_train: np.ndarray, y_train: np.ndarray) -> float:
    """
    Compute the out-of-bag score for the RandomForestClassifier.
    """
    n_samples = X_train.shape[0]
    n_classes = len(forest.classes_)
    votes = np.zeros((n_samples, n_classes), dtype=int)

    for tree, inbag in zip(forest.estimators_, forest.estimators_samples_):
        oob_idx = np.setdiff1d(np.arange(n_samples), inbag, assume_unique=True).astype(int)
        if oob_idx.size == 0:
            continue

        preds = tree.predict(X_train[oob_idx]).astype(int)

        for sample_idx, pred in zip(oob_idx, preds):
            votes[sample_idx, pred] += 1

    voted_mask = votes.sum(axis=1) > 0
    oob_preds = votes.argmax(axis=1)

    return np.mean(oob_preds[voted_mask] == y_train[voted_mask])


def FreeModel(forest: RandomForestClassifier) -> None:
    """
    Free the memory used by the forest.
    """
    del forest
    gc.collect()

    return 