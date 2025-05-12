import numpy as np

"""
https://github.com/RRdmlearning/Machine-Learning-From-Scratch/blob/master/gradient_boosting_decision_tree/gbdt_model.py
"""

class sq_error_Loss:
    def __init__(self): 
        pass

    def loss(self, y, y_pred):
        return 0.5 * np.power((y - y_pred), 2)

    def gradient(self, y, y_pred):
        return -(y - y_pred)


class abs_error_Loss:
    def __init__(self): 
        pass

    def loss(self, y, y_pred):
        return np.abs(y - y_pred)

    def gradient(self, y, y_pred):
        return np.less(y,y_pred).astype('float')*2-1
        