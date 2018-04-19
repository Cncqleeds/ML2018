import numpy as np 
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D

URL = "https://archive.ics.uci.edu/ml/machine-learning-databases/optdigits/"

digits_train = pd.read_csv(URL+"/optdigits.tra",header=None)
digits_test = pd.read_csv(URL+"/optdigits.tes",header=None)

x_train = digits_train[np.arange(64)]
y_train = digits_train[64]

x_test = digits_test[np.arange(64)]
y_test = digits_test[64]

estimator = PCA(n_components=3)
x_train_pca = estimator.fit_transform(x_train)
x_test_pca = estimator.transform(x_test)

def plot_pca_scatter():
    colors = ['black','blue','purple','yellow','white','red','lime','cyan','orange','gray']
    fig = plt.figure()
    ax = Axes3D(fig)
    for i in range(len(colors)):
        px = x_train_pca[:,0][y_train.as_matrix()==i]
        py = x_train_pca[:,1][y_train.as_matrix()==i]
        pz = x_train_pca[:,2][y_train.as_matrix()==i]
        ax.scatter(px,py,pz,c=colors[i])
    
    ax.set_zlabel('Third Principal Component')
    ax.set_ylabel('Second Principal Component')
    ax.set_xlabel('First Principal Component')
    ax.legend(np.arange(0,10).astype(str))
    ax.view_init(50,50)

    plt.show()
	
plot_pca_scatter()