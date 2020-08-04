import numpy as np
from .metrics import r2_score

class SimpleLineaRegression1:
    def __init__(self):
        self.a_=None
        self.b_=None

    def fit(self,x_train,y_trian):
        assert x_train.ndim==1,\
            'Simple Linear Regrssor can only solve single feature training data.'
        assert len(x_train)==len(y_trian),\
            'the size of x_train must be equal to the size of y_train'
        x_mean=np.mean(x_train)
        y_mean=np.mean(y_trian)
        num=0.0
        d=0.0
        for x,y in zip(x_train,y_trian):
            num+=(x-x_mean)*(y-y_mean)
            d+=(x-x_mean)**2
        self.a_=num/d
        self.b_=y_mean-self.a_*x_mean
        return self

    def predict(self,x_predict):
        assert x_predict.ndim==1,\
            'Simple Linear Regressor can only solve single feature training data.'
        assert self.a_ is not None and self.b_ is not None,\
            'must fit before predict'
        return np.array([self._predict(x) for x in x_predict])

    def _predict(self,x_single):
        return self.a_*x_single+self.b_

    def __repr__(self):
        return 'SimpleLineaRegression1()'


class SimpleLineaRegression2:
    def __init__(self):
        self.a_=None
        self.b_=None

    def fit(self,x_train,y_trian):
        assert x_train.ndim==1,\
            'Simple Linear Regrssor can only solve single feature training data.'
        assert len(x_train)==len(y_trian),\
            'the size of x_train must be equal to the size of y_train'
        x_mean=np.mean(x_train)
        y_mean=np.mean(y_trian)
        num=(x_train-x_mean).dot(y_trian-y_mean)
        d=(x_train-x_mean).dot(x_train-x_mean)
        self.a_=num/d
        self.b_=y_mean-self.a_*x_mean
        return self

    def predict(self,x_predict):
        assert x_predict.ndim==1,\
            'Simple Linear Regressor can only solve single feature training data.'
        assert self.a_ is not None and self.b_ is not None,\
            'must fit before predict'
        return np.array([self._predict(x) for x in x_predict])

    def _predict(self,x_single):
        return self.a_*x_single+self.b_

    def score(self,x_test,y_test):
        y_predict=self.predict(x_test)
        return r2_score(y_test,y_predict)
    
    def __repr__(self):
        return 'SimpleLineaRegression2()'