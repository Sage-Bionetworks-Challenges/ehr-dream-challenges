import numpy as np
import sklearn
from sklearn.metrics import average_precision_score
from sklearn.linear_model import LogisticRegressionCV
import warnings
import scipy
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=FutureWarning)
from scipy.sparse import vstack
from sys import getsizeof
import sklearn
import tensorflow as tf
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

# train on synthetic data and test on real data
death = np.load("../shuffled_death.npy")
alive = np.load("../shuffled_alive.npy")
combine = np.concatenate((alive,death),axis = 0)
y= [0]*alive.shape[0]+[1]*death.shape[0]
y = np.array(y)
shuffled_x = np.empty(combine.shape, dtype=combine.dtype)
shuffled_y = np.empty(y.shape, dtype=y.dtype)
permutation = np.random.permutation(len(combine))
print(permutation)
for old_index, new_index in enumerate(permutation):
    shuffled_x[new_index] = combine[old_index]
    shuffled_y[new_index] = y[old_index]
shuffled_y =  shuffled_y.reshape((y.shape[0], 1))
def shuffle(matrix, target, test_proportion):
    ratio = int(matrix.shape[0]/test_proportion) #should be int
    X_train = matrix[ratio:,:]
    X_test =  matrix[:ratio,:]
    Y_train = target[ratio:,:]
    Y_test =  target[:ratio,:]
    return X_train, X_test, Y_train, Y_test
x_train, x_test, y_train, y_test = shuffle(shuffled_x, shuffled_y, 5)
n_samples = alive.shape[0]+death.shape[0]

'''load real data'''
deathr = np.load("../death.npy")
aliver = np.load("../alive.npy")
combiner = np.concatenate((aliver,deathr),axis = 0)
yr= [0]*aliver.shape[0]+[1]*deathr.shape[0]
yr = np.array(yr)
shuffled_xr = np.empty(combiner.shape, dtype=combiner.dtype)
shuffled_yr = np.empty(yr.shape, dtype=yr.dtype)
permutationr = np.random.permutation(len(combiner))
for old_indexr, new_indexr in enumerate(permutationr):
    shuffled_xr[new_indexr] = combiner[old_indexr]
    shuffled_yr[new_indexr] = yr[old_indexr]
shuffled_yr =  shuffled_yr.reshape((yr.shape[0], 1))
'''load real_data'''
'''load infer data'''
infer_gold = pd.read_csv('../goldstandard5.csv')
yi = np.array(infer_gold['status'])
xi = np.load("../infer5.npy")
'''load infer data'''
#model.fit(shuffled_x,shuffled_y)
'''
## model train on synthetic data
model.fit(shuffled_x,shuffled_y)
print("print coeficient")
coef = model.coef_
coef = coef.reshape((10697,1))
coef_list_syn = pd.DataFrame(coef, columns = ['coef'])
print(type(coef_list_syn))
print(coef_list_syn)
print(coef_list_syn.shape)
coef_list_syn.to_csv('coef_medWGAN.csv',index = False)
y_pred1 = model.predict_proba(shuffled_xr)[:,1]
y_pred2 = model.predict_proba(xi)[:,1]
model2 = LogisticRegression(penalty = 'l2', tol = 0.0001,random_state = None, max_iter = 1500)
print("shape")
print(x_train.shape)
print(y_train.shape)
print(x_test.shape)
print(y_test.shape)
model2.fit(x_train,y_train)
y_pred3 = model2.predict_proba(x_test)[:,1]
print(y_pred3.shape)
score1 = sklearn.metrics.roc_auc_score(shuffled_yr, y_pred1)
score2 = sklearn.metrics.roc_auc_score(yi, y_pred2)
score3 = sklearn.metrics.roc_auc_score(y_test, y_pred3)
score4 = average_precision_score(shuffled_yr, y_pred1)
score5 = average_precision_score(yi, y_pred2)
score6 = average_precision_score(y_test, y_pred3)
print("score on train real{}".format(score1),flush = True)
print("score on infer real{}".format(score2),flush = True)
print("score on itself{}".format(score3),flush = True)
print("prauc score on train real{}".format(score4),flush = True)
print("prauc score on infer real{}".format(score5),flush = True)
print("prauc score on itself{}".format(score6),flush = True)
'''
#score4 = sklearn.metrics.f1_score(shuffled_yr, y_pred1)
#score5 = sklearn.metrics.f1_score(yi, y_pred2)
#score6 = sklearn.metrics.f1_score(shuffled_y, y_pred3)
#print("f1 score on train real{}".format(score4),flush = True)
#print("f1 score on infer real{}".format(score5),flush = True)
#print("f1 score on itself{}".format(score6),flush = True)
model = LogisticRegressionCV(penalty = 'l2', tol = 0.001,random_state = None)
#model = RandomForestClassifier(n_estimators=100, max_depth=20)
model.fit(shuffled_x,shuffled_y)
print("print coeficient")
coef = model.coef_
#coef = model.feature_importances_
coef = coef.reshape((10697,1))
coef_list_syn = pd.DataFrame(coef, columns = ['coef'])
print(type(coef_list_syn))
print(coef_list_syn)
print(coef_list_syn.shape)
coef_list_syn.to_csv('../coef/coef_shuffled.csv',index = False)
y_pred1 = model.predict_proba(shuffled_x)[:,1]
y_pred2 = model.predict_proba(xi)[:,1]
y_pred3 = model.predict_proba(shuffled_xr)[:,1]
print(y_pred3.shape)
score1 = sklearn.metrics.roc_auc_score(shuffled_y, y_pred1)
score2 = sklearn.metrics.roc_auc_score(yi, y_pred2)
score3 = sklearn.metrics.roc_auc_score(shuffled_yr, y_pred3)
score4 = average_precision_score(shuffled_y, y_pred1)
score5 = average_precision_score(yi, y_pred2)
score6 = average_precision_score(shuffled_yr, y_pred3)
print("score on syn_train_shuffled{}".format(score1),flush = True)
print("score on infer_train on shuffled{}".format(score2),flush = True)
print("score on real_train on shuffled{}".format(score3),flush = True)
print("prauc score on syn_train_shuffled{}".format(score4),flush = True)
print("prauc score on infer_train_shuffled{}".format(score5),flush = True)
print("prauc score on real__train_shuffled{}".format(score6),flush = True)
