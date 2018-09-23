
import pandas as pd 

df=pd.DataFrame([1,2,3])


print(df)


import numpy as np
import matplotlib.pyplot as plt
import glob

weights_path=r'D:\Deep learning_NPTEL\weights'

wf_list=glob.glob(weights_path+'\*.npy')

from sklearn.metrics import  M  
from sklearn.metrics import mean_sqaured_error
from sklearn.metrics import mean_squared_error

def sigmoid(x,w):
    return 1 /(1 + np.e ** -((w *x)))

def loss(y,y_hat):
    print(y.shape,y_hat.shape)
    return mean_squared_error(y,y_hat)
#def sigma(x):
#    return 1 / (1 + np.exp(-x))


def train_loss(y,data,pred_w):
    tr=loss(y,sigmoid(data,pred_w))
    
    return tr


def test_loss(y,data,pred_w):
    ts=loss(y,sigmoid(data,pred_w))
    return ts


traindata=pd.read_csv(r'D:\Deep learning_NPTEL\data\training_data.csv')
valdata=pd.read_csv(r'D:\Deep learning_NPTEL\data\validation_data.csv')
traindata.head()

data=traindata.iloc[:,:-1].values
y=traindata['Y'].values

vdata=valdata.iloc[:,:-1].values
valy=valdata['Y'].values

tr_list=[]
val_list=[]
for wf in wf_list:
    pred_w=np.load(wf)
    tr_list.append(train_loss(y,data,pred_w))
    val_list.append(test_loss(valy,vdata,pred_w))

plt.plot(tr_list,label='tr')
plt.plot(val_list)
plt.legend()
plt.show()