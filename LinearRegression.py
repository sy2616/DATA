import numpy as np
from .metrics import r2_score

class LinearRegression:
    def __init__(self):
        self.coef_=None
        self.interception_=None
        self._theta=None

    def fit_normal(self,X_train,y_train):
        assert X_train.shape[0]==y_train.shape[0],\
            'the size of X_train must be equal to the sizeof y_train'
        X_b=np.hstack([np.ones((len(X_train),1)),X_train])
        self._theta=np.linalg.inv(X_b.T.dot(X_b)).dot((X_b.T)).dot(y_train)
        self.interception_=self._theta[0]
        self.coef_=self._theta[1:]
        return self

    def fit_gd(self,X_train,y_train,eta=0.01,n_iters=1e4):
        assert X_train.shape[0]==y_train.shape[0],\
            'the size of X_train must be equal to the size of y_train'
        def J(theta, x_b, y):
            try:
                return np.sum((y - x_b.dot(theta)) ** 2) / len(x_b)
            except:
                return float('inf')

        def dJ(theta, x_b, y):
            # res = np.empty(len(theta))
            # res[0] = np.sum(x_b.dot(theta) - y)
            # for i in range(1, len(theta)):
            #     res[i] = (x_b.dot(theta) - y).dot(x_b[:, i])
            # return res * 2 / len(x_b)
            return x_b.T.dot(x_b.dot(theta)-y)*2/len(x_b)
        def gradient_descent(x_b, y, initial_theta, eta, n_iters=1e4, epsilon=1e-8):
            theta = initial_theta
            i_iter = 0
            while i_iter < n_iters:
                gradient = dJ(theta, x_b, y)
                last_theta = theta
                theta = theta - eta * gradient
                if (abs(J(theta, x_b, y) - J(last_theta, x_b, y)) < epsilon):
                    break
                i_iter += 1
            return theta
        x_b=np.hstack([np.ones((len(X_train),1)),X_train])
        initial_theta=np.zeros(x_b.shape[1])
        self._theta=gradient_descent(x_b,y_train,initial_theta,eta,n_iters=1e4, epsilon=1e-8)
        self.interception_=self._theta[0]
        self.coef_=self._theta[1:]
        return self

    def fit_sgd(self,X_train,y_train,n_iters=5,t0=5,t1=50):
        assert X_train.shape[0]==y_train.shape[0],\
            'the size of X_train must be equal to the size of y_train'
        assert n_iters>=1
        def dJ_sgd(theta,x_b_i,y_i):
            return x_b_i*(x_b_i.dot(theta)-y_i)*2.
        def sgd(x_b,y,initial_theta,n_iters,t0=5,t1=50):
            def learning_rate(t):
                return t0/(t+t1)

            theta=initial_theta
            m=len(x_b)
            for cur_iter in range(n_iters):
                indexs=np.random.permutation(m)
                x_b_new=x_b[indexs]
                y_new=y[indexs]
                for i in range(m):
                    gradient=dJ_sgd(theta,x_b_new[i],y_new[i])
                    theta=theta-learning_rate(cur_iter*m+i)*gradient

            return theta
        x_b=np.hstack([np.ones((len(X_train),1)),X_train])
        initial_theta=np.random.randint(x_b.shape[1])
        self._theta=sgd(x_b,y_train,initial_theta,n_iters,t0,t1)
        self.interception_=self._theta[0]
        self.coef_=self._theta[1:]
        return self

    def predict(self,X_predict):
        assert self.interception_ is not None and self.coef_ is not None,\
            'must fit before predict'
        assert X_predict.shape[1]==len(self.coef_),\
            'the feature number of X_predict must be equal to X_train'
        X_b = np.hstack([np.ones((len(X_predict), 1)), X_predict])
        return X_b.dot(self._theta)

    def score(self,X_test,y_test):
        y_predict=self.predict(X_test)
        return r2_score(y_test,y_predict)

    def __repr__(self):
        return 'LinearRegression()'
