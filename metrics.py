import numpy as np

def accuracy_score(y_true,y_predict):
    assert y_true.shape[0]==y_predict.shape[0],\
        'the size of y_true must be equal to the sze of y_predict'
    return sum(y_true==y_predict)/len(y_true)

def mean_squared_error(y_ture,y_predict):
    assert len(y_ture)==len(y_predict),\
        'the size of y_ture must be equal to the size of y_predict'
    return np.sum((y_ture-y_predict)**2)/len(y_ture)

def root_mean_squared_error(y_ture,y_predict):
    return squr(mean_squared_error(y_ture,y_predict))

def mean_absolute_error(y_ture,y_predict):
    assert len(y_ture)==len(y_predict),\
        'the size of y_ture must be equal to the size of y_predict'
    return np.sum(np.absolute(y_ture-y_predict))/len(y_ture)

def r2_score(y_ture,y_predict):
    return 1-mean_squared_error(y_ture,y_predict)/np.var(y_ture)