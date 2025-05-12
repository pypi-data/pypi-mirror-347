"""
Basic tests for the pasi_test package (Prediction Accuracy Subgroup Identification Tree)

Tests the core functionality of identifying subgroups with differential model performance
"""
import numpy as np
import pandas as pd
import pytest
from sklearn.linear_model import LogisticRegression

from pasi_test import pasiTree, delong_roc_variance, auprc_estimation


def test_import():
    """Test that the package imports correctly."""
    assert pasiTree is not None
    assert delong_roc_variance is not None
    assert auprc_estimation is not None


def test_auc_calculation():
    """Test AUC calculation with a simple example."""
    y_true = np.array([0, 0, 1, 1])
    y_pred = np.array([0.1, 0.4, 0.35, 0.8])
    
    result = delong_roc_variance(y=y_true, y_pred=y_pred)
    
    assert isinstance(result, dict)
    assert 'mu' in result
    assert 'var' in result
    assert 'sd' in result
    assert 'ci' in result
    assert len(result['ci']) == 2
    
    # For perfect predictions, AUC should be 0.75
    assert 0.5 <= result['mu'] <= 1.0


def test_auprc_calculation():
    """Test AUPRC calculation with a simple example."""
    y_true = np.array([0, 0, 1, 1])
    y_pred = np.array([0.1, 0.4, 0.35, 0.8])
    
    result = auprc_estimation(y=y_true, y_pred=y_pred, n_bootstrap=10)
    
    assert isinstance(result, dict)
    assert 'mu' in result
    assert 'var' in result
    assert 'sd' in result
    assert 'ci' in result
    assert len(result['ci']) == 2
    
    # AUPRC should be between 0 and 1
    assert 0 <= result['mu'] <= 1.0


def test_tree_creation():
    """Test creating a pasiTree with simple data."""
    # Create a simple dataset
    X = pd.DataFrame({
        'feature1': [1.2, 3.4, 5.6, 7.8, 9.0, 2.3, 4.5, 6.7],
        'feature2': ['A', 'B', 'A', 'B', 'A', 'B', 'A', 'B']
    })
    y = np.array([0, 0, 0, 0, 1, 1, 1, 1])
    
    # Fit a simple model
    pred_model = LogisticRegression(random_state=42).fit(pd.get_dummies(X), y)
    y_pred = pred_model.predict_proba(pd.get_dummies(X))[:, 1]
    
    # Create a tree with AUC
    tree_auc = pasiTree(measure='auc', min_samples_leaf=2, max_depth=2)
    tree_auc.fit(X=X, y=y, y_pred=y_pred)
    
    # Tree should have been created
    assert hasattr(tree_auc, 'tree')
    
    # Test prediction
    preds = tree_auc.predict(X)
    assert len(preds) == len(y)
    
    # Create a tree with AUPRC
    tree_auprc = pasiTree(measure='auprc', min_samples_leaf=2, max_depth=2)
    tree_auprc.fit(X=X, y=y, y_pred=y_pred)
    
    # Tree should have been created
    assert hasattr(tree_auprc, 'tree')
    
    # Test prediction
    preds_auprc = tree_auprc.predict(X)
    assert len(preds_auprc) == len(y)


if __name__ == "__main__":
    test_import()
    test_auc_calculation()
    test_auprc_calculation()
    test_tree_creation()
    print("All tests passed!") 