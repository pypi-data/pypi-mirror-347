import pandas as pd
import numpy as np
from sklearn.model_selection import KFold
from sklearn.utils import resample
from scipy.stats import norm, uniform, bernoulli
from scipy.optimize import minimize

import functools
import itertools
from joblib import Parallel, delayed
import copy
import platform
import progressbar

from .acc_functions import indiv_acc_estimation, delong_roc_variance, auprc_estimation
from .loss_functions import sq_error_Loss, abs_error_Loss





class Node:
    def __init__(self, train_acc, train_sd, train_ci, n_train, measure, idx):
        self.train_acc = train_acc
        self.train_sd = train_sd
        self.train_ci = train_ci
        self.n_train = n_train
        self.measure = measure
        self.idx = idx  # node index

        #self.left = None
        #self.right = None
        #self.feature_index = None
        #self.threshold = None

        #self.train_s = None
        #self.total_s = None
        #self.internal_cnt = None
        #self.g = None

        #self.test_acc = None
        #self.test_sd = None
        #self.test_ci = None
        #self.n_test = None
        self.real_test_acc = None # indicator of whether test acc is calculated from real test obs or simply copied from train acc

        self.min_pos_neg_leaf_auc = 5
        
        # For AUPRC we need more examples of the minority class
        if self.measure == 'auprc':
            self.min_pos_neg_leaf_auc = 10

        self._node_checks()

        if self.measure == 'indiv':
            self.acc_func = indiv_acc_estimation
        elif self.measure == 'auprc':
            self.acc_func = auprc_estimation
        else:
            self.acc_func = delong_roc_variance


    def _is_leaf(self):
        if hasattr(self, "left") and hasattr(self, "right"):
            return False
        elif not hasattr(self, "left") and not hasattr(self, "right"):
            return True
        else:
            raise Exception("Unclear if node is terminal. Check!!")
    

    def _node_checks(self):
        assert self.measure in ['indiv', 'auc', 'auprc']


    def _check_and_modify_input(self, X: pd.DataFrame, mu=None, y=None, y_pred=None):
        assert isinstance(X, pd.DataFrame)
        n = X.shape[0]

        if self.measure == 'indiv':
            assert isinstance(mu, np.ndarray) 
            assert y is None or np.isnan(y).sum() == n
            assert y_pred is None or np.isnan(y_pred).sum() == n
            assert mu.shape == (n,)
            y,y_pred = np.array([np.nan]*n),np.array([np.nan]*n)
        else:
            assert isinstance(y, np.ndarray) and isinstance(y_pred, np.ndarray)
            assert mu is None or np.isnan(mu).sum() == n
            assert y.shape == (n,) and y_pred.shape == (n,)
            mu = np.array([np.nan]*n)
        
        return X, mu, y, y_pred


    def _compute_pruning_statistics(self):
        """
        Compute and set total_s and internal_cnt for the input node and all of its descendants.
        :param node: a tree node
        :return: total_s and internal_cnt for the input node
        """
        is_leaf = self._is_leaf()
        # if node is terminal, return
        if is_leaf:
            self.train_s, self.total_s, self.internal_cnt, self.g = None, None, None, None
            # return (total_s, internal_cnt) as (0, 0)
            return 0, 0
        else:
            # compute total_s, internal_cnt for the left child node
            left_total_s, left_internal_cnt = self.left._compute_pruning_statistics()
            # compute total_s, internal_cnt for the right child node
            right_total_s, right_internal_cnt = self.right._compute_pruning_statistics()

            self.total_s = left_total_s + right_total_s + self.train_s
            self.internal_cnt = left_internal_cnt + right_internal_cnt + 1
            self.g = self.total_s / self.internal_cnt

            return self.total_s, self.internal_cnt


    def _get_g_values(self) -> list:
        """
        Retrieve the g values of a given node and all of its descendants.
        :param node: a tree node
        :return: a list of (node idx, g value) for the node and all of its descendants
        """
        is_leaf = self._is_leaf()
        if is_leaf:
            return [(self.idx, None)]
        else:
            left_g_values = self.left._get_g_values()
            right_g_values = self.right._get_g_values()
            return [(self.idx, self.g)] + left_g_values + right_g_values
    

    def _prune(self, node_idx_2_prune):
        is_leaf = self._is_leaf()
        if not is_leaf:
            if self.idx == node_idx_2_prune:
                delattr(self, "left")
                delattr(self, "right")
                delattr(self, "feature_index")
                delattr(self, "threshold")
                #self.left = None
                #self.right = None
                #self.feature_index = None
                #self.threshold = None
            else:
                self.left._prune(node_idx_2_prune)
                self.right._prune(node_idx_2_prune)


    def _compute_total_s(self, X: pd.DataFrame, mu: np.ndarray, y: np.ndarray, y_pred: np.ndarray):
        """
        Compute total_s and internal count when a fitted tree/node is applied to (potentially new/unseen/test) data: X,mu,y,y_pred
        """
        
        X, mu, y, y_pred = self._check_and_modify_input(X, mu, y, y_pred)
        n = X.shape[0]

        is_leaf = self._is_leaf()
        if is_leaf:
            total_s, internal_cnt = 0, 0
            return total_s, internal_cnt

        if isinstance(self.threshold, list):
            x = X.iloc[:, [self.feature_index]].to_numpy(dtype='str', copy=True).reshape((n,))
            # left_idx = np.array([x[i] in node.threshold for i in range(len(x))])
            left_idx = np.isin(x, self.threshold)
        else:
            x = X.iloc[:, [self.feature_index]].to_numpy(dtype='float', copy=True).reshape((n,))
            left_idx = (x <= self.threshold)  # boolean array

        # if this split results in either left or right child node having no observation, then treat split as None
        if left_idx.sum() == 0 or (~left_idx).sum() == 0:
            total_s, internal_cnt = 0, 0
            return total_s, internal_cnt

        left_X, left_mu, left_y, left_y_pred = X.loc[left_idx,:], mu[left_idx], y[left_idx], y_pred[left_idx]
        right_X, right_mu, right_y, right_y_pred = X.loc[~left_idx,:], mu[~left_idx], y[~left_idx], y_pred[~left_idx]
        if self.measure in ['auc', 'auprc']:
            # the numbers of pos and neg samples in either subgroup must both be >= min_pos_neg_leaf_auc
            if (left_y == 1).sum() < self.min_pos_neg_leaf_auc or (left_y == 0).sum() < self.min_pos_neg_leaf_auc or (right_y == 1).sum() < self.min_pos_neg_leaf_auc or (right_y == 0).sum() < self.min_pos_neg_leaf_auc:
                total_s, internal_cnt = 0, 0
                return total_s, internal_cnt

        left_acc_est, right_acc_est = self.acc_func(left_mu, left_y, left_y_pred), self.acc_func(right_mu, right_y, right_y_pred)
        
        nu = (left_acc_est['mu'] - right_acc_est['mu']) ** 2
        de = left_acc_est['var'] + right_acc_est['var']
        if de <= 0:
            return 0, 0
        s = nu / de

        left_total_s, left_internal_cnt = self.left._compute_total_s(left_X, left_mu, left_y, left_y_pred)
        right_total_s, right_internal_cnt = self.right._compute_total_s(right_X, right_mu, right_y, right_y_pred)
        # print(node.idx,nu,de,a,b,c,d,s)
        return left_total_s + right_total_s + s, left_internal_cnt + right_internal_cnt + 1


    def export_graphviz(self, feature_names=None, show_n_sample=True, precision=3, measure_name=None, show_ci=True):
        if feature_names is None:
            feature_names = ['X{}'.format(j) for j in range(100000)]
        
        if measure_name is None:
            measure_name = 'acc'
        
        tree_dot_data = 'digraph Tree {node [shape=box, style="rounded", color="black", fontname="helvetica"] ;edge [fontname="helvetica"] ;'
        tree_dot_data += self._export_graphviz(feature_names=feature_names, show_n_sample=show_n_sample, precision=precision, measure_name=measure_name, show_ci=show_ci)
        tree_dot_data += '}'

        return tree_dot_data#, graphviz.Source(tree_dot_data,format='png')

    
    def _export_graphviz(self, feature_names:list, show_n_sample:bool, precision:int, measure_name:str, show_ci:bool):
        is_leaf = self._is_leaf()
        
        show_pruning_stats = False

        train_acc = round(self.train_acc, precision)
        if is_leaf:
            out = '{} [style=bold; label=<node {}<br/>train {} = {}'.format(self.idx, self.idx, measure_name, train_acc)
        else:
            out = '{} [label=<node {}<br/>train {} = {}'.format(self.idx, self.idx, measure_name, train_acc)


        if show_ci:
            #train_sd = self.train_sd
            train_ci_lower = round(self.train_ci[0], precision)
            train_ci_upper = round(self.train_ci[1], precision)
            out += ' ({}, {})'.format(train_ci_lower, train_ci_upper)

        if show_n_sample:
            out += '<br/>n_train = {}'.format(self.n_train)


        if self.real_test_acc is not None:
            test_acc = round(self.test_acc, precision)
            if self.real_test_acc:
                out += '<br/>test {} = {}'.format(measure_name, test_acc)
            else:
                out += '<br/>test {} = {}*'.format(measure_name, test_acc)
            if show_ci:
                test_ci_lower = round(self.test_ci[0], precision)
                test_ci_upper = round(self.test_ci[1], precision)
                out += ' ({}, {})'.format(test_ci_lower, test_ci_upper)
            if show_n_sample:
                out += '<br/>n_test = {}'.format(self.n_test)
        
        
        if show_pruning_stats and not is_leaf:
            out += '<br/>train_s = {}'.format(round(self.train_s,precision))
            out += '<br/>total_s = {}'.format(round(self.total_s,precision))
            out += '<br/>internal_cnt = {}'.format(self.internal_cnt)
            out += '<br/>g = {}'.format(round(self.g,precision))



        if is_leaf:
            out += '>];'
        else:
            if isinstance(self.threshold, list):
                out += "<br/>{} in {}".format(feature_names[self.feature_index], self.threshold)
            else:
                out += "<br/>{} &le; {}".format(feature_names[self.feature_index], round(self.threshold,precision))
            out += '>];'
            left = self.left._export_graphviz(feature_names=feature_names,show_n_sample=show_n_sample,precision=precision,measure_name=measure_name,show_ci=show_ci)
            right = self.right._export_graphviz(feature_names=feature_names,show_n_sample=show_n_sample,precision=precision,measure_name=measure_name,show_ci=show_ci)
            out += left
            out += right


        # connect this node to its parent node
        if self.idx > 1:
            if self.idx % 2 == 0:
                out += '{} -> {};'.format(int(self.idx/2),self.idx)
            else:
                out += '{} -> {};'.format(int((self.idx-1)/2),self.idx)

        return out

        
    def _single_predict(self, x: pd.Series, mode: str):
        """
        x is covariate vector for a single observation. pd series with shape=(p,)
        """
        node = self
        assert isinstance(x, pd.Series) and len(x.shape) == 1, 'x: invalid input'
        assert mode in ['train', 'test']

        while not node._is_leaf():
            if isinstance(node.threshold, list):
                if x[node.feature_index] in node.threshold:
                    node = node.left
                else:
                    node = node.right
            else:
                if x[node.feature_index] <= node.threshold:
                    node = node.left
                else:
                    node = node.right
        
        if mode == 'train':
            return node.train_acc, node.idx
        else:
            return node.test_acc, node.idx


    def predict(self, X: pd.DataFrame, mode='train'):
        """
        :param node: a node object
        :param X: a pd dataframe with dim n*p
        :param mode: either value or idx
        :return: a np array of predictions for each x in X
        """
        assert mode in ['train', 'test']
        
        preds = X.apply(func=lambda x: self._single_predict(x, mode=mode), axis=1, result_type="expand")

        return preds[0].to_numpy()


    def _test_eval(self, X: pd.DataFrame, mu: np.ndarray, y: np.ndarray, y_pred: np.ndarray, real_test_acc=True):
        """
        Compute test_acc,test_sd,test_ci,n_test when a fitted tree/node is applied to (potentially new/unseen/test) data: X,mu,y,y_pred
        """

        if X is None:
            assert real_test_acc == False

        if real_test_acc:
            result = self.acc_func(mu, y, y_pred)
            self.test_acc, self.test_sd, self.test_ci = result['mu'], result['sd'], result['ci']
            self.n_test = y.shape[0]
            self.real_test_acc = True # indicator of whether test acc is calculated from real test obs or simply copied from train acc
        else:
            # not calculating real test acc
            self.test_acc, self.test_sd, self.test_ci = self.train_acc, self.train_sd, self.train_ci

            if X is not None:
                # there are test obs fall in this node
                self.n_test = y.shape[0]
            else:
                # no test obs fall in this node
                self.n_test = 0

            self.real_test_acc = False


        is_leaf = self._is_leaf()
        if is_leaf:
            return self

        # node has child nodes (not terminal)

        ## no test obs in this node

        if X is None:
            # so all child nodes must also have no test obs, that is X and y are None and real_test_acc=False
            self.left._test_eval(X=None, mu=None, y=None, y_pred=None, real_test_acc=False)
            self.right._test_eval(X=None, mu=None, y=None, y_pred=None, real_test_acc=False)
            return self


        ## there are test obs in current node
        n = X.shape[0]

        if isinstance(self.threshold, list):
            x = X.iloc[:, [self.feature_index]].to_numpy(dtype='str', copy=True).reshape((n,))
            left_idx = np.isin(x, self.threshold)
        else:
            x = X.iloc[:, [self.feature_index]].to_numpy(dtype='float', copy=True).reshape((n,))
            left_idx = (x <= self.threshold)  # boolean array

        if left_idx.sum() == 0:  
            # no test obs fall into left branch
            # this means there must be test obs in the right branch
            self.left._test_eval(X=None, mu=None, y=None, y_pred=None, real_test_acc=False)
            
            right_X, right_mu, right_y, right_y_pred = X.loc[~left_idx,:], mu[~left_idx], y[~left_idx], y_pred[~left_idx]
            if self.measure in ['auc', 'auprc']:
                # the numbers of pos and neg samples in right branch must both be >= min_pos_neg_leaf_auc
                if (right_y == 1).sum() < self.min_pos_neg_leaf_auc or (right_y == 0).sum() < self.min_pos_neg_leaf_auc:
                    self.right._test_eval(right_X, right_mu, right_y, right_y_pred, real_test_acc=False)
                else:
                    self.right._test_eval(right_X, right_mu, right_y, right_y_pred, real_test_acc=real_test_acc)
            else:
                self.right._test_eval(right_X, right_mu, right_y, right_y_pred, real_test_acc=real_test_acc)
        
        elif (~left_idx).sum() == 0:  
            # no test obs in right branch but obs in left branch
            self.right._test_eval(X=None, mu=None, y=None, y_pred=None, real_test_acc=False)

            left_X, left_mu, left_y, left_y_pred = X.loc[left_idx,:], mu[left_idx], y[left_idx], y_pred[left_idx]
            if self.measure in ['auc', 'auprc']:
                # the numbers of pos and neg samples in left branch must both be >= min_pos_neg_leaf_auc
                if (left_y == 1).sum() < self.min_pos_neg_leaf_auc or (left_y == 0).sum() < self.min_pos_neg_leaf_auc:
                    self.left._test_eval(left_X, left_mu, left_y, left_y_pred, real_test_acc=False)
                else:
                    self.left._test_eval(left_X, left_mu, left_y, left_y_pred, real_test_acc=real_test_acc)
            else:
                self.left._test_eval(left_X, left_mu, left_y, left_y_pred, real_test_acc=real_test_acc)
        else:
            # there are obs in both left and right branch
            left_X, left_mu, left_y, left_y_pred = X.loc[left_idx,:], mu[left_idx], y[left_idx], y_pred[left_idx]
            right_X, right_mu, right_y, right_y_pred = X.loc[~left_idx,:], mu[~left_idx], y[~left_idx], y_pred[~left_idx]
            if self.measure in ['auc', 'auprc']:
                # the numbers of pos and neg samples in either subgroup must both be >= min_pos_neg_leaf_auc
                if (left_y == 1).sum() < self.min_pos_neg_leaf_auc or (left_y == 0).sum() < self.min_pos_neg_leaf_auc:
                    self.left._test_eval(left_X, left_mu, left_y, left_y_pred, real_test_acc=False)

                    if (right_y == 1).sum() < self.min_pos_neg_leaf_auc or (right_y == 0).sum() < self.min_pos_neg_leaf_auc:
                        self.right._test_eval(right_X, right_mu, right_y, right_y_pred, real_test_acc=False)
                    else:
                        self.right._test_eval(right_X, right_mu, right_y, right_y_pred, real_test_acc=real_test_acc)
                else:
                    self.left._test_eval(left_X, left_mu, left_y, left_y_pred, real_test_acc=real_test_acc)
                    if (right_y == 1).sum() < self.min_pos_neg_leaf_auc or (right_y == 0).sum() < self.min_pos_neg_leaf_auc:
                        self.right._test_eval(right_X, right_mu, right_y, right_y_pred, real_test_acc=False)
                    else:
                        self.right._test_eval(right_X, right_mu, right_y, right_y_pred, real_test_acc=real_test_acc)
            else:
                self.left._test_eval(left_X, left_mu, left_y, left_y_pred, real_test_acc=real_test_acc)
                self.right._test_eval(right_X, right_mu, right_y, right_y_pred, real_test_acc=real_test_acc)




class pasiTree:
    def __init__(self, measure='indiv', max_depth=100, min_samples_split=None, min_samples_leaf=2, max_features='auto', random_state=19301014):
        # values set upon creation of pasiTree object
        self.measure = measure 
        self.max_depth = max_depth
        self.min_samples_leaf = min_samples_leaf
        self.min_samples_split = min_samples_split if min_samples_split is not None else min_samples_leaf*2
        self.max_features = max_features
        self.random_state = random_state # controls random covariate selection when max_feature != auto
        
        self.min_pos_neg_leaf_auc = 5 # min number of pos/neg obs in resulting child nodes for split to be valid when measure is auc


        self._model_checks()

        if self.measure == 'indiv': 
            self.acc_func = indiv_acc_estimation
        elif self.measure == 'auprc':
            self.acc_func = auprc_estimation
        else:
            self.acc_func = delong_roc_variance
        
        #self.scp_alphas = None
        #self.scp_betas = None
        #self.subtree_seq_list = None
        #self.alpha_prime = None
        #self.cart_mode = None
        #self.n_fold = None
        #self.best_alpha = None
        #self.best_alpha_idx = None
        #self.beta_cv_dict = None
        #self.final_tree_dot, self.final_tree_graph = None, None
        

    def _model_checks(self):
        assert self.measure in ['indiv', 'auc', 'auprc']
        assert self.max_features in ['auto', 'sqrt']

        self.max_depth = min(self.max_depth, 100)

        if self.measure == 'indiv':
            self.min_samples_leaf = max(self.min_samples_leaf, 2)
        else:
            self.min_samples_leaf = max(self.min_samples_leaf, 50)

        self.min_samples_split = max(self.min_samples_split, self.min_samples_leaf*2)


    def _check_and_modify_input(self, X: pd.DataFrame, mu=None, y=None, y_pred=None):
        assert isinstance(X, pd.DataFrame), 'X should be a pandas dataframe'
        
        # check dtypes of X
        for k in X.dtypes.to_dict().keys():
            if X.dtypes.to_dict()[k] not in ['int64', 'float64', 'string']:
                raise Exception('Dtype of column {} must be one of [int64, float64, string]'.format(k))
            
        n = X.shape[0]

        if self.measure == 'indiv':
            assert isinstance(mu, np.ndarray) and mu.shape == (n,)
            assert y is None or np.isnan(y).sum() == n
            assert y_pred is None or np.isnan(y_pred).sum() == n
            y, y_pred = np.array([np.nan]*n), np.array([np.nan]*n)
        else:
            assert isinstance(y, np.ndarray) and isinstance(y_pred, np.ndarray)
            assert mu is None or np.isnan(mu).sum() == n
            assert y.shape == (n,) and y_pred.shape == (n,)
            assert set(y) == {0.0, 1.0}
            mu = np.array([np.nan]*n)
        
        return X, mu, y, y_pred


    def _is_fitted(self):
        return hasattr(self, "tree")


    def _is_pruned(self):
        return hasattr(self, "pruned_tree")


    def _is_test_evaluated(self):
        if hasattr(self, "test_evaluated"):
            return self.test_evaluated
        else:
            return False


    def fit(self, X: pd.DataFrame, mu=None, y=None, y_pred=None):

        ########## Run checks before fitting PASI tree ##########
        X, mu, y, y_pred = self._check_and_modify_input(X, mu, y, y_pred)

        ########## build full-grown tree T0 ##########
        self.tree = self._grow_tree(X=X, mu=mu, y=y, y_pred=y_pred, depth=0, node_idx=1)
        self.tree_dot = self.tree.export_graphviz(feature_names=list(X.columns))

        return self
    

    def split_complexity_pruning_path(self):
        assert self._is_fitted(), "fit model first"

        self.tree._compute_pruning_statistics()

        subtree_seq_list = [copy.deepcopy(self.tree)]
        scp_alphas = [0.0]

        # while the current smallest subtree contains more than the root node
        while not subtree_seq_list[-1]._is_leaf():
            Tm = copy.deepcopy(subtree_seq_list[-1])
            g_list = Tm._get_g_values()
            node2prune_idx, node2prune_alpha = min([x for x in g_list if x[1]], key=lambda i: i[1])
            scp_alphas.append(node2prune_alpha)
            Tm._prune(node2prune_idx)
            Tm._compute_pruning_statistics()
            subtree_seq_list.append(Tm)

        self.scp_alphas = scp_alphas
        self.subtree_seq_list = subtree_seq_list

        return scp_alphas, subtree_seq_list


    def predict(self, X: pd.DataFrame, mode='train') -> np.ndarray:
        assert self._is_fitted(), "fit model first"
        if mode == 'test':
            assert self._is_test_evaluated
        
        if self._is_pruned():
            return self.pruned_tree.predict(X, mode)
        else:
            return self.tree.predict(X, mode)


    def test_eval(self, X: pd.DataFrame, mu=None, y=None, y_pred=None):
        assert self._is_fitted(), "fit model first"

        X, mu, y, y_pred = self._check_and_modify_input(X, mu, y, y_pred)
        
        if self._is_pruned():
            self.pruned_tree._test_eval(X, mu, y, y_pred, real_test_acc=True)
        else:
            self.tree._test_eval(X, mu, y, y_pred, real_test_acc=True)
        
        self.test_evaluated = True

        return self


    def select_pruned_tree(self, X: pd.DataFrame, mu=None, y=None, y_pred=None, n_fold=5, cart_mode=False, alpha_prime=4, cv_seed=19301014):
        assert self._is_fitted(), "fit model first"
        assert alpha_prime in [0, 2, 3, 4]
        if cart_mode:
            assert self.measure == 'indiv', 'cart mode is only available when acc is available at indiv level'

        X, mu, y, y_pred = self._check_and_modify_input(X, mu, y, y_pred)

        self.alpha_prime = alpha_prime
        self.cart_mode = cart_mode
        self.n_fold = n_fold
        self.cv_seed = cv_seed
        
        self.split_complexity_pruning_path()
        n_alphas = len(self.scp_alphas)
        scp_betas = [np.sqrt(self.scp_alphas[i] * self.scp_alphas[i + 1]) for i in range(n_alphas - 1)] + [np.inf]
        n_betas = len(scp_betas)

        kf = KFold(n_splits=n_fold, shuffle=True, random_state=self.cv_seed)
        beta_cv_dict = {}
        for m in range(n_betas):
            beta_cv_dict[str(m)] = []
        
        fold_id = 0
        for train_index, test_index in kf.split(X):
            fold_id += 1
            #print(fold_id)
            train_X, train_mu, train_y, train_y_pred = X.iloc[train_index,:], mu[train_index], y[train_index], y_pred[train_index]
            test_X, test_mu, test_y, test_y_pred = X.iloc[test_index,:], mu[test_index], y[test_index], y_pred[test_index]
            
            cv_model = pasiTree(max_depth=self.max_depth, min_samples_leaf=self.min_samples_leaf, measure=self.measure, min_samples_split=self.min_samples_split, max_features=self.max_features, random_state=19301014)
            cv_model = cv_model.fit(train_X, train_mu, train_y, train_y_pred)
            cv_model.split_complexity_pruning_path()
            
            for m in range(n_betas):
                beta = scp_betas[m]
                kf_subtree_idx = max(i for i in range(len(cv_model.scp_alphas)) if beta >= cv_model.scp_alphas[i])
                kf_subtree4beta = copy.deepcopy(cv_model.subtree_seq_list[kf_subtree_idx])
                if not cart_mode:
                    total_s, internal_cnt = kf_subtree4beta._compute_total_s(test_X, test_mu, test_y, test_y_pred)
                    if kf_subtree4beta.internal_cnt is not None:
                        if alpha_prime != 0:
                            beta_cv_dict[str(m)].append(total_s - alpha_prime*1.0 * kf_subtree4beta.internal_cnt)
                        else:
                            beta_cv_dict[str(m)].append(total_s - np.log(test_y.shape[0]) * kf_subtree4beta.internal_cnt)
                    else:
                        beta_cv_dict[str(m)].append(0)
                else:
                    # predict the pseudo-response for each observation in test_X
                    pred_pseudo_outcome = kf_subtree4beta.predict(test_X)
                    # true pseudo-response for each test x
                    true_pseudo_outcome = test_mu # since measure='indiv', mu is pseudo-response 
                    # make this negative so we want to maximize
                    neg_cv_error = -np.mean((true_pseudo_outcome - pred_pseudo_outcome) ** 2)
                    beta_cv_dict[str(m)].append(neg_cv_error)

        beta_cv_mean = [np.mean(beta_cv_dict[m]) for m in beta_cv_dict.keys()]
        best_alpha_idx = np.argmax(beta_cv_mean)
        best_alpha = self.scp_alphas[best_alpha_idx]

        self.best_alpha = best_alpha
        self.best_alpha_idx = best_alpha_idx
        self.pruned_tree = copy.deepcopy(self.subtree_seq_list[best_alpha_idx])
        self.scp_betas = scp_betas
        self.beta_cv_dict = beta_cv_dict
        self.pruned_tree_dot = self.pruned_tree.export_graphviz(feature_names=list(X.columns))

        return self


    def _grow_tree(self, X: pd.DataFrame, mu: np.ndarray, y: np.ndarray, y_pred: np.ndarray, depth=0, node_idx=1):
        
        n = X.shape[0]

        # compute acc of current node
        acc_result = self.acc_func(mu=mu, y=y, y_pred=y_pred)
        
        # instantiate current node
        node = Node(train_acc=acc_result['mu'], train_sd=acc_result['sd'], train_ci=np.array(acc_result['ci']), n_train=n, measure=self.measure, idx=node_idx)

        # recursively split until stopping rules are met
        if depth < self.max_depth and node.n_train >= self.min_samples_split:
            feat_idx, thr, s = self._best_split(X=X, mu=mu, y=y, y_pred=y_pred, node_idx=node_idx)


            #print('feat idx:',feat_idx,'thr:',thr,'s:',s)
            if feat_idx is not None:
                node.feature_index, node.threshold, node.train_s = feat_idx, thr, s

                # check data type at column index=idx
                #continuous = not isinstance(X.iat[0, feat_idx], str)
                continuous = not isinstance(X.dtypes[feat_idx], pd.StringDtype)
                data_type = 'float64' if continuous else 'str'
                x = X.iloc[:, [feat_idx]].to_numpy(dtype=data_type).reshape((n,))
                if continuous:
                    left_idx = (x <= thr)
                else:
                    left_idx = np.isin(x, thr)
                
                #try:
                assert left_idx.sum() > 0 and (~left_idx).sum() > 0
                #except AssertionError:
                #    print('feat_idx={}, thr={}, node_idx={}'.format(feat_idx, thr, node_idx))
                #    cut_pts,_ = self._get_cut_pts(x=x,mu=mu,y=y,y_pred=y_pred)
                #    print('cut_pts:',cut_pts[-5:],'unique x:',np.unique(x)[-5:])

                X_left, mu_left, y_left, y_pred_left = X[left_idx], mu[left_idx], y[left_idx], y_pred[left_idx]
                X_right, mu_right, y_right, y_pred_right = X[~left_idx], mu[~left_idx], y[~left_idx], y_pred[~left_idx]
                #print('y_left',y_left)

                node.left = self._grow_tree(X_left, mu_left, y_left, y_pred_left, depth + 1, node_idx * 2)
                node.right = self._grow_tree(X_right, mu_right, y_right, y_pred_right, depth + 1, node_idx * 2 + 1)


        return node

    
    def _best_split(self, X: pd.DataFrame, mu: np.ndarray, y: np.ndarray, y_pred: np.ndarray, node_idx: int):

        # Initialize best split variables
        best_idx = None
        best_thr = None
        best_s = 0.0

        n_features = X.shape[1]

        # Pre-convert DataFrame to NumPy array for faster column access
        X_arr = X.to_numpy()

        # Determine which feature indices to consider (avoid inline lambda by direct delayed call)
        if self.max_features == 'sqrt':
            num_feats = int(np.sqrt(n_features))
            rng = np.random.default_rng(node_idx + self.random_state)
            feat_indices = rng.choice(n_features, size=num_feats, replace=False)
        else:
            feat_indices = list(range(n_features))

        # Parallel evaluation of each feature's best split without inline lambda
        results = Parallel(n_jobs=-1)(
            delayed(self._process_each_feature)(X_arr[:, i], mu, y, y_pred, i)
            for i in feat_indices
        )

        # Choose the split with the highest score
        feat_idx, thr, s = max(results, key=lambda tup: tup[2])
        if s > best_s:
            best_s = s
            best_thr = thr
            best_idx = feat_idx

        return best_idx, best_thr, best_s


    def _process_each_feature(self, x: np.ndarray, mu: np.ndarray, y: np.ndarray, y_pred: np.ndarray, feat_idx: int):

        if isinstance(x, pd.Series):
            categorical = True if isinstance(x.iloc[0],str) else False
            x = x.to_numpy() if categorical else x.to_numpy(dtype='float64')
        else:
            assert isinstance(x, np.ndarray)
            categorical = True if isinstance(x[0],str) else False
            if not categorical:
                x = x.astype('float64')

        n = x.shape[0]

        cut_pts, sort_idx = self._get_cut_pts(x=x, mu=mu, y=y, y_pred=y_pred)

        #print(cut_pts)
        
        thr, s = None, 0.0

        if cut_pts is None:
            return feat_idx, thr, s

        
        if sort_idx is not None:
            # sort_idx is None only when efficient=False
            if not categorical and self.measure in ['auc', 'auprc'] and len(cut_pts)>4000:
                print('using multiprocessing')
                results = Parallel(n_jobs=-1)(delayed(lambda cut_pt: self._single_split(cut_pt, x, mu, y, y_pred))(cut_pt) for cut_pt in cut_pts)
                thr, s = max(results, key=lambda i: i[1])
                if s == 0:
                    thr = None
            else:
                x = x[sort_idx]
                mu = mu[sort_idx]
                y = y[sort_idx]
                y_pred = y_pred[sort_idx]

                #print(x)

                i = 0
                for j in range(1,n):
                    if x[j] != x[0]:
                        break
                    i += 1

                cut_pt_idx = 0
                s = 0
                thr = None
                best_cut_pt_idx = None
                n_left_pos = y[:i+1].sum()
                n_left_neg = 0
                n_right_pos = (y==1).sum()-n_left_pos
                n_right_neg = 0
                eq_cnt = 0

                #print(x,i)
                while i < n-1:

                    n_left = i+1
                    n_right = n - n_left

                    #print(cut_pts[cut_pt_idx])

                    if self.measure in ['auc', 'auprc']:
                        #print(y[(i+1-eq_cnt):i+1])
                        n_left_pos += y[(i+1-eq_cnt):i+1].sum()
                        n_left_neg = n_left - n_left_pos
                        n_right_pos -= y[i+1-eq_cnt:i+1].sum()
                        n_right_neg = n_right - n_right_pos


                    split_checks_ok = False
                    if n_left >= self.min_samples_leaf and n_right >= self.min_samples_leaf:
                        if self.measure in ['auc', 'auprc']:
                            if n_left_pos >= self.min_pos_neg_leaf_auc and n_left_neg >= self.min_pos_neg_leaf_auc and n_right_pos >= self.min_pos_neg_leaf_auc and n_right_neg >= self.min_pos_neg_leaf_auc:
                                split_checks_ok = True
                        else:
                            split_checks_ok = True
                    #split_checks_ok = True
                    if split_checks_ok:
                        left_mu, right_mu = mu[:i+1], mu[i+1:]
                        left_y, right_y, left_y_pred, right_y_pred = y[:i+1], y[i+1:], y_pred[:i+1], y_pred[i+1:]

                        #assert n_left_pos == left_y.sum()
                        #assert n_left_neg == (1-left_y).sum()
                        #assert n_right_pos == right_y.sum()
                        #assert n_right_neg == (1-right_y).sum()

                        #print(left_y,right_y)

                        left_acc_est, right_acc_est = self.acc_func(left_mu, left_y, left_y_pred), self.acc_func(right_mu, right_y, right_y_pred)
                        nu = (left_acc_est['mu'] - right_acc_est['mu']) ** 2
                        de = left_acc_est['var'] + right_acc_est['var']

                        #print(cut_pts[cut_pt_idx], nu/de, n_left,n_right,n_left_pos,n_left_neg,n_right_pos,n_right_neg)

                        if de > 0:
                            if nu/de > s:
                                s = nu/de
                                thr = cut_pts[cut_pt_idx]
                                #best_cut_pt_idx = cut_pt_idx

                    eq_cnt = 0
                    for j in range(i+1,n):
                        if x[j] == x[i+1]:
                            eq_cnt += 1
                        else:
                            break
                        
                        
                    #print(i,eq_cnt,cut_pt_idx,n_left,n_right,x[:i+1],x[i+1:],cut_pts[cut_pt_idx])
                    cut_pt_idx += 1
                    i += eq_cnt if eq_cnt > 0 else 1
        else:
            # this is when sort_idx is None, i.e. categorical x with efficient=False
            for left_c in cut_pts:

                result = self._single_split(cut_pt=left_c, x=x, mu=mu, y=y, y_pred=y_pred)

                if result[1] > s:
                    thr, s = result[0], result[1]

        return feat_idx, thr, s


    def _get_cut_pts(self, x: np.ndarray, mu: np.ndarray, y: np.ndarray, y_pred: np.ndarray):

        categorical = True if isinstance(x[0], str) else False

        if not categorical:
            sorted_unique_x = np.sort(np.unique(x))
            if sorted_unique_x.shape[0] < 2:
                cut_pts, sort_idx = None, None
                return cut_pts, sort_idx
            cut_pts = (sorted_unique_x[1:] + sorted_unique_x[:-1]) / 2.0
            sort_idx = np.argsort(x)
        else:
            cat = np.unique(x)
            if cat.shape[0] < 2:  # if there is only one category in x, then skip this feature
                cut_pts, sort_idx = None, None
                return cut_pts, sort_idx

            if self.measure in ['auc', 'auprc']:
                # Since AUPRC is particularly sensitive to having enough minority class examples,
                # we should ensure each category has sufficient samples of both classes
                min_samples = 2
                if self.measure == 'auprc':
                    min_samples = 3  # Higher threshold for AUPRC to ensure stability
                efficient = (set([c for c in cat if (y[x == c] == 1).sum() >= min_samples and (y[x == c] == 0).sum() >= min_samples]) == set(cat))
            else:
                efficient = True

            if efficient:
                cat_acc = np.array([self.acc_func(mu[x == c], y[x == c], y_pred[x == c])['mu'] for c in cat])
                sorted_cat = list(cat[np.argsort(cat_acc)])
                cut_pts = [sorted_cat[:i+1] for i in range(len(sorted_cat)-1)]

                dummy = dict([(c,i) for i,c in enumerate(sorted_cat)])
                sort_idx = np.argsort([dummy[e] for e in x])
            else:
                cut_pts = [[list(q) for q in itertools.combinations(cat, l)] for l in range(1, len(cat))]
                cut_pts = functools.reduce(lambda a, b: a + b, cut_pts)
                [cut_pts.remove(c) for c in cut_pts if set(cat.tolist()) in [set(c1 + c) for c1 in cut_pts]]
                sort_idx = None

        return cut_pts, sort_idx


    def _single_split(self, cut_pt, x: np.ndarray, mu: np.ndarray, y: np.ndarray, y_pred: np.ndarray):
        """
        Evaluates the quality of a single potential split point for a feature.
        
        This function determines how good a specific split would be by calculating a quality score
        that represents the normalized difference between accuracy measures in the resulting branches.
        The function handles both categorical and numerical features, and implements measure-specific
        checks for different accuracy metrics (indiv, auc, auprc).
        
        Parameters
        ----------
        cut_pt : float or list
            The threshold value for numerical features, or a list of categories for categorical features
            that would comprise the left branch.
        x : np.ndarray
            Feature values for all samples.
        mu : np.ndarray
            Individual accuracy values when measure='indiv', or NaN array otherwise.
        y : np.ndarray
            Binary target values (0/1) when measure='auc' or 'auprc', or NaN array otherwise.
        y_pred : np.ndarray
            Predicted probabilities when measure='auc' or 'auprc', or NaN array otherwise.
            
        Returns
        -------
        tuple
            (cut_pt, quality_score) where quality_score is a float representing the quality of the split.
            Higher values indicate better splits. A score of 0 indicates an invalid or worthless split.
            The score is computed as: (diff_in_accuracy)² / (sum_of_variances)
        
        Notes
        -----
        - For categorical features, left_idx is determined by checking which values are in cut_pt.
        - For numerical features, left_idx is determined by checking which values are <= cut_pt.
        - Splits that would create child nodes with too few samples are rejected (score = 0).
        - For AUC and AUPRC measures, additional checks ensure both classes have enough samples.
        - The quality score accounts for both the magnitude of the split effect and its reliability.
        """
        categorical = True if isinstance(x[0],str) else False

        if categorical:
            left_idx = np.isin(x, cut_pt)
        else:
            left_idx = (x <= cut_pt)  # boolean (mask) array

        n_left, n_right = (left_idx).sum(), (~left_idx).sum()

        if n_left < self.min_samples_leaf or n_right < self.min_samples_leaf:
        # if either subgroup has samples less than min_sample_leaf, then t is inadmissible
            return cut_pt, 0.0


        left_mu, right_mu = mu[left_idx], mu[~left_idx]
        left_y, right_y, left_y_pred, right_y_pred = y[left_idx], y[~left_idx], y_pred[left_idx], y_pred[~left_idx]

        if self.measure in ['auc', 'auprc']:
            if (left_y == 1).sum() < self.min_pos_neg_leaf_auc or (left_y == 0).sum() < self.min_pos_neg_leaf_auc or (right_y == 1).sum() < self.min_pos_neg_leaf_auc or (right_y == 0).sum() < self.min_pos_neg_leaf_auc:
                return cut_pt,0.0


        left_acc_est, right_acc_est = self.acc_func(left_mu, left_y, left_y_pred), self.acc_func(right_mu, right_y, right_y_pred)


        nu = (left_acc_est['mu'] - right_acc_est['mu']) ** 2
        de = left_acc_est['var'] + right_acc_est['var']

        if de > 0:
            return cut_pt,nu/de

        return cut_pt,0.0



