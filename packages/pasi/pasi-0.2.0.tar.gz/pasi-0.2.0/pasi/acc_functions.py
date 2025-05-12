from numba import jit
import numpy as np
from scipy import stats
from sklearn.metrics import average_precision_score
from sklearn.utils import resample
from joblib import Parallel, delayed









#@jit(nopython=True,parallel=False)
def indiv_acc_estimation(mu:np.ndarray, y=None, y_pred=None):
    """ Estimate of individual-level accuracy and estimate of variance
    outcomes is np array with shape=(N,)
    E.g., for MSE estimation, outcomes should be squared errors. For MAE estimation, outcomes should be absolute errors. 
    For classification error rate (cer) estimation, outcomes should be binary errors (I(y!=y_hat)). 
    """
    N = mu.shape[0]
    mu_hat = mu.mean()
    var_hat = mu.var() / N

    # 95% CI, normal approximation
    c = 1.96
    sd_hat = np.sqrt(var_hat)
    ci_l = mu_hat-c*sd_hat
    ci_u = mu_hat+c*sd_hat

    
    return {'mu': mu_hat, 'var': var_hat, 'sd': sd_hat, 'ci':[ci_l, ci_u]}



@jit(nopython=True,parallel=False)
def compute_midrank(x):
    """Computes midranks.
    Args:
       x - a 1D numpy array
    Returns:
       array of midranks
    """
    J = np.argsort(x)
    Z = x[J]
    N = len(x)
    T = np.zeros(N, dtype=np.float64)
    i = 0
    while i < N:
        j = i
        while j < N and Z[j] == Z[i]:
            j += 1
        T[i:j] = 0.5*(i + j - 1)
        i = j
    T2 = np.empty(N, dtype=np.float64)
    # Note(kazeevn) +1 is due to Python using 0-based indexing
    # instead of 1-based in the AUC formula in the paper
    T2[J] = T + 1
    return T2

def fastDeLong(predictions_sorted_transposed, label_1_count):
    # Short variables are named as they are in the paper
    m = label_1_count
    n = predictions_sorted_transposed.shape[1] - m
    positive_examples = predictions_sorted_transposed[:, :m]
    negative_examples = predictions_sorted_transposed[:, m:]
    k = predictions_sorted_transposed.shape[0]
    
    
    tx = np.empty((k, m), dtype=np.float64)
    ty = np.empty((k, n), dtype=np.float64)
    tz = np.empty((k, m + n), dtype=np.float64)
    for r in range(k):
        tx[r, :] = compute_midrank(positive_examples[r, :])
        ty[r, :] = compute_midrank(negative_examples[r, :])
        tz[r, :] = compute_midrank(predictions_sorted_transposed[r, :])
    aucs = tz[:, :m].sum(axis=1) / m / n - float(m + 1.0) / 2.0 / n
    v01 = (tz[:, :m] - tx[:, :]) / n
    v10 = 1.0 - (tz[:, m:] - ty[:, :]) / m


    #np.seterr(divide='raise')
    #try:
    #    sx = np.cov(v01[0])
    #except FloatingPointError:
    #    print(v01,m,n,k)
    #    print(v01.shape)
    #    print(v01[0].shape)

    sx = np.cov(v01[0])
    sy = np.cov(v10[0])
    delongcov = sx / m + sy / n
    return aucs, delongcov

def compute_ground_truth_statistics(ground_truth):
    assert np.array_equal(np.unique(ground_truth), [0, 1]), '{}'.format(np.unique(ground_truth))
        
    order = (-ground_truth).argsort()
    label_1_count = int(ground_truth.sum())
    return order, label_1_count

def delong_roc_variance(mu=None, y=None, y_pred=None):
    """
    Computes ROC AUC variance for a single set of predictions
    Args:
       ground_truth: np.array of 0 and 1
       predictions: np.array of floats of the probability of being class 1
    """

    if y.shape[0] < 1:
        return auc_estimation(mu,y,y_pred)

    order, label_1_count = compute_ground_truth_statistics(y)
    predictions_sorted_transposed = y_pred[np.newaxis, order]
    aucs, delongcov = fastDeLong(predictions_sorted_transposed, label_1_count)
    assert len(aucs) == 1, "There is a bug in the code, please forward this to the developers"
    #return aucs[0], delongcov

    mu = aucs[0]
    alpha = 0.95
    mu_std = np.sqrt(delongcov)
    lower_upper_q = np.abs(np.array([0, 1]) - (1 - alpha) / 2)
    
    if mu_std > 0:
        ci = stats.norm.ppf(lower_upper_q,loc=mu,scale=mu_std)
    else:
        ci = np.array([0.0, 0.0])
    ci[ci > 1] = 1
    ci[ci < 0] = 0

    return {'mu': mu, 'var': delongcov, 'sd': mu_std, 'ci':[ci[0], ci[1]]}




# def auc_estimation_Shirahata(y:np.array, y_pred:np.array) -> dict:
#     """
#     Estimate the AUC and its variance using the formula from Shirahata [1993].
    
#     Parameters:
#     - y (np.array): True binary responses (0/1) with shape (N,).
#     - y_pred (np.array): Predicted scores with shape (N,).

#     Returns:
#     - dict: A dictionary containing the following key-value pairs:
#         * 'mu': Estimated AUC
#         * 'var': Estimated variance of mu
#         * 'sd': Estimated standard error of mu
#         * 'ci': 95% confidence interval for AUC (based on the normal approximation)
#         * 'm': Number of positive samples
#         * 'n': Number of negative samples
#         * 'B': Sum of the number of times each positive sample score exceeds each negative sample score

#     Raises:
#     - ValueError: If `y` and `y_pred` have different lengths.
#     - ValueError: If all labels in `y` are positive or all are negative.
    
#     Notes:
#     - The method is based on Shirahata [1993]. https://www.jstage.jst.go.jp/article/jjscs1988/6/2/6_2_1/_article
#     """
#     # Check for mismatched sizes
#     if len(y) != len(y_pred):
#         raise ValueError(f"Input arrays y and y_pred must have the same size. {len(y)} != {len(y_pred)}")
    
#     # Check if y and y_pred have shape (N,)
#     if y.shape != (len(y),) or y_pred.shape != (len(y_pred),):
#         raise ValueError("Both y and y_pred must have a shape of (N,).")
    
#     pos_array = y_pred[y == 1]
#     neg_array = y_pred[y == 0]
#     m = float(len(pos_array))
#     n = float(len(neg_array))

#     # Check for all positive or all negative
#     if m == 0:
#         raise ValueError("Positive labels must be present in y.")
    
#     if n == 0:
#         raise ValueError("Negative labels must be present in y.")


#     c_array = np.sum(pos_array[:, np.newaxis] > neg_array, axis=1)
#     d_array = np.sum(neg_array[:, np.newaxis] < pos_array, axis=1)

#     c_square = np.sum(c_array ** 2)
#     d_square = np.sum(d_array ** 2)
#     B = np.sum(c_array)

#     denominator = m * n
#     if m > 1:
#         denominator *= (m - 1)
#     if n > 1:
#         denominator *= (n - 1)
    
#     var_hat = (-(m + n - 1) * B ** 2 / (m * n) - B + c_square + d_square) / denominator
    
#     # 95% CI, normal approximation
#     mu = B / (m * n)
#     sd_hat = np.sqrt(var_hat)
#     alpha = 0.95
#     lower_upper_q = np.abs(np.array([0, 1]) - (1 - alpha) / 2)

#     if sd_hat > 0:
#         ci = stats.norm.ppf(lower_upper_q, loc=mu, scale=sd_hat)
#     else:
#         ci = np.array([0.0, 0.0])
#     ci[ci > 1] = 1
#     ci[ci < 0] = 0

#     return {'mu': mu, 'var': var_hat, 'sd': sd_hat, 'ci':[ci[0], ci[1]], 'm': m, 'n': n, 'B': B}




def auc_estimation_HM(y:np.array, y_pred:np.array) -> dict:
    """
    Compute the Area Under the Curve (AUC) and its variance for a given set of true labels and predictions.
    
    This function calculates the AUC using the trapezoidal method and then estimates its variance. 
    Additionally, it provides a 95% confidence interval for the AUC based on the normal approximation.
    
    Parameters:
    -----------
    y : numpy.ndarray
        A one-dimensional array of true labels. Must contain only binary values (0s and 1s) 
        where 1 denotes the positive class and 0 denotes the negative class.
    
    y_pred : numpy.ndarray
        A one-dimensional array of prediction scores corresponding to each sample in `y`. 
        Higher scores are assumed to indicate positive class preference.
    
    Returns:
    --------
    dict
        A dictionary containing:
        - 'mu': Estimated AUC
        - 'var': Estimated variance of AUC
        - 'sd': Standard deviation (square root of variance)
        - 'ci': 95% confidence interval for the AUC (as a list of two values: lower and upper bounds)
        - 'm': Number of positive samples
        - 'n': Number of negative samples
    
    Raises:
    -------
    ValueError:
        - If `y` and `y_pred` are not both numpy arrays.
        - If shapes of `y` and `y_pred` don't match or they are not 1-dimensional.
        - If `y` contains values other than 0 or 1.
        
    Notes:
    ------
    The function uses the trapezoidal rule to compute the AUC and a known formula to estimate its variance.
    Hanley, J. A., & McNeil, B. J. (1982). The meaning and use of the area under a receiver operating characteristic (ROC) curve. Radiology, 143(1), 29-36.
    """


    # Check that y and y_pred are numpy arrays
    if not (isinstance(y, np.ndarray) and isinstance(y_pred, np.ndarray)):
        raise ValueError("Both y and y_pred must be numpy arrays.")
    
    # Check that y and y_pred have the same shape and is of shape (N,)
    if y.shape != y_pred.shape or len(y.shape) != 1:
        raise ValueError("y and y_pred must have the same shape of (N,).")
    
    # Check that y contains only 0s and 1s
    if not np.array_equal(np.unique(y), [0, 1]) and not np.array_equal(np.unique(y), [1, 0]):
        raise ValueError("y should contain 0s and 1s.")
    
    # Calculate number of positive and negative samples
    m = np.sum(y)
    n = len(y_pred) - m

    # Sort the samples by ascending scores
    sorted_indices = np.argsort(y_pred)
    y_true_sorted = y[sorted_indices]

    # Vectorized calculation of cumulative sum for true positive and false positive
    cum_tpr = np.cumsum(y_true_sorted) / m
    cum_fpr = np.cumsum(1 - y_true_sorted) / n

    # Compute AUC using the trapezoid method
    auc = np.sum((cum_tpr[1:] - cum_tpr[:-1]) * (cum_fpr[1:] + cum_fpr[:-1])) / 2

    # Estimate variance using the updated formula
    auc2 = auc * auc
    Q1 = auc / (2 - auc)
    Q2 = 2 * auc2 / (1 + auc)
    var_auc = (auc * (1 - auc) + (m - 1) * (Q1 - auc2) + (n - 1) * (Q2 - auc2)) / (m * n)

    # 95% CI, normal approximation
    sd_hat = np.sqrt(var_auc)
    alpha = 0.95
    lower_upper_q = np.abs(np.array([0, 1]) - (1 - alpha) / 2)

    if sd_hat > 0:
        ci = stats.norm.ppf(lower_upper_q, loc=auc, scale=sd_hat)
    else:
        ci = np.array([0.0, 0.0])
    ci[ci > 1] = 1
    ci[ci < 0] = 0

    return {'mu': auc, 'var': var_auc, 'sd': sd_hat, 'ci':[ci[0], ci[1]], 'm':m, 'n': n}

def auprc_estimation(mu=None, y=None, y_pred=None, n_bootstrap:int=1000, random_seed:int=None, n_jobs:int=-1) -> dict:
    """
    Compute the Area Under the Precision-Recall Curve (AUPRC) and estimate its variance.
    
    This function calculates the AUPRC using sklearn's average_precision_score and 
    estimates its variance using stratified bootstrap resampling that preserves the
    class distribution of the original dataset.
    
    Parameters:
    -----------
    mu : numpy.ndarray, default=None
        Not used for AUPRC calculation, included for interface consistency.
    
    y : numpy.ndarray
        A one-dimensional array of true labels. Must contain only binary values (0s and 1s) 
        where 1 denotes the positive class and 0 denotes the negative class.
    
    y_pred : numpy.ndarray
        A one-dimensional array of prediction scores corresponding to each sample in `y`. 
        Higher scores are assumed to indicate positive class preference.
        
    n_bootstrap : int, default=1000
        Number of bootstrap iterations for variance estimation.
        
    random_seed : int, default=None
        Random seed for reproducibility.
        
    n_jobs : int, default=-1
        Number of jobs for parallel processing. -1 means using all processors.
    
    Returns:
    --------
    dict
        A dictionary containing:
        - 'mu': Estimated AUPRC
        - 'var': Estimated variance of AUPRC
        - 'sd': Standard deviation (square root of variance)
        - 'ci': 95% confidence interval for the AUPRC
    
    Raises:
    -------
    ValueError:
        - If `y` and `y_pred` have different lengths.
        - If `y` contains values other than 0 or 1.
        
    Notes:
    ------
    The function uses sklearn's average_precision_score to compute AUPRC and
    stratified bootstrap resampling to estimate variance.
    """
    # Convert to numpy arrays if they aren't already
    y = np.asarray(y)
    y_pred = np.asarray(y_pred)
    
    # Set random seed if provided
    if random_seed is not None:
        np.random.seed(random_seed)
    
    # Input validation (fast checks first)
    if len(y) != len(y_pred):
        raise ValueError(f"Input arrays y and y_pred must have the same size. {len(y)} != {len(y_pred)}")
    
    # Use faster check instead of np.all(np.isin())
    unique_values = np.unique(y)
    if not (len(unique_values) <= 2 and np.all(unique_values <= 1) and np.all(unique_values >= 0)):
        raise ValueError("y should contain only 0s and 1s.")
    
    # Ensure both classes are present
    if len(unique_values) < 2:
        raise ValueError("Both positive and negative classes must be present in y.")
    
    # Calculate AUPRC
    auprc = average_precision_score(y, y_pred)
    
    # Create indices for resampling
    indices = np.arange(len(y))
    
    # Define a function for parallel bootstrap iteration
    def bootstrap_iteration(i):
        # Use different random state for each iteration
        state = None if random_seed is None else random_seed + i
        indices_resampled = resample(indices, n_samples=len(indices), stratify=y, random_state=state, replace=True)
        return average_precision_score(y[indices_resampled], y_pred[indices_resampled])
    
    # Parallel bootstrap processing
    bootstrap_scores = np.array(Parallel(n_jobs=n_jobs)(
        delayed(bootstrap_iteration)(i) for i in range(n_bootstrap)
    ))
    
    # Calculate variance and standard deviation
    var_auprc = np.var(bootstrap_scores)
    sd_auprc = np.sqrt(var_auprc)
    
    # 95% confidence interval - use faster method with pre-sorted array
    bootstrap_scores.sort()  # In-place sort is faster
    alpha = 0.95
    lower_idx = int((1 - alpha) / 2 * n_bootstrap)
    upper_idx = int((1 + alpha) / 2 * n_bootstrap)
    
    # Ensure indices are within bounds
    lower_idx = max(0, lower_idx)
    upper_idx = min(n_bootstrap - 1, upper_idx)
    
    ci_lower = bootstrap_scores[lower_idx]
    ci_upper = bootstrap_scores[upper_idx]
    
    return {'mu': auprc, 'var': var_auprc, 'sd': sd_auprc, 'ci': [ci_lower, ci_upper]}



