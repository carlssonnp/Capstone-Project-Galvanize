import pandas as pd
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans, DBSCAN
import numpy as np

def load_wave(filename):
    with open(filename,'r') as f:
        names = next(f) # skip first row
        df = pd.DataFrame(l.rstrip().split(',') for l in f)
    return df,names

def load_waves():
    dfs = []
    for i in xrange(1,7):
        filename = 'WV' + str(i) + '.dat'
        dfs.append(load_wave(filename).iloc[:,0:80])
    return dfs

def load_longitudinal():
    with open('WVS_Longitudinal_1981_2014_sas_v2015_04_18.dat','r') as f:
        next(f) # skip first row
        #for i in xrange(10):
        # test = f.readline()
        #df = pd.DataFrame(test)
        df = pd.DataFrame(l.rstrip().split('-') for l in f)
    #return df
    return df

# def combine_waves(dfs):
#     #for df in dfs:
#     pass


if __name__ == '__main__':
    scaler = StandardScaler()
    k = KMeans(8)
    dfs =load_waves()
    #longitudinal = load_longitudinal()
    pca = PCA()
    dfs[5] = dfs[5].convert_objects(convert_numeric = True)
    # dfs[5] = dfs[5].replace(-5,1)
    # dfs[5] = dfs[5].replace(-4,1)
    # dfs[5] = dfs[5].replace(-3,1)
    # dfs[5] = dfs[5].replace(-2,1)
    # dfs[5] = dfs[5].replace(-1,1)
    for i in xrange(5,60):
        dfs[5].iloc[:,i] = dfs[5].iloc[:,i].replace(-5,2)
        dfs[5].iloc[:,i] = dfs[5].iloc[:,i].replace(-4,2)
        dfs[5].iloc[:,i] = dfs[5].iloc[:,i].replace(-3,2)
        dfs[5].iloc[:,i] = dfs[5].iloc[:,i].replace(-2,2)
        dfs[5].iloc[:,i] = dfs[5].iloc[:,i].replace(-1,2)
    transformed = pca.fit_transform(dfs[5].iloc[:,5:10])
    df_trans = pd.DataFrame(transformed)
    df_trans['country'] = dfs[5].iloc[:,1]
    group = df_trans.groupby('country').mean()
    plt.scatter(group.iloc[:,0], group.iloc[:,1])
    one = transformed[:,0]
    one = scaler.fit_transform(one)
    two = transformed[:,1]
    two = scaler.fit_transform(two)
    #two = 1000*two
    both = np.vstack((one,two)).T
    k.fit(both)
    plt.scatter(two, one, c = k.labels_)




#print(df)
