import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.datasets import load_iris
from sklearn.externals import joblib

iris = load_iris()

X = iris.data
y = iris.target

idxs = np.random.permutation(len(X))

X_train = X[idxs[:-10]]
y_train = y[idxs[:-10]]

X_test = X[idxs[-10:]]
y_test = y[idxs[-10:]]

clf = KNeighborsClassifier()
clf.fit(X_train, y_train)

joblib.dump(clf, 'model.pkl')