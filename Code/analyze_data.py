from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans, DBSCAN
import numpy as np
from read_data import load_csv, load_stata
import pandas as pd
from statsmodels.regression.linear_model import OLS, WLS
from statsmodels.api import add_constant

def create_columns(num_vars):
    col_nums = xrange(1,num_vars + 1)
    columns = [('A00' + str(col_num)) if col_num <10 else ('A0' + str(col_num)) for col_num in col_nums]
    return columns

def choose_columns(df_in,columns):
    df_out = df_in.ix[:,columns]
    return df_out


def remove_negatives(df_in):
    for column in df_in.columns:
        column_mean = df_in[df_in[column] > 0][column].mean()
        df_in[column] = df_in[column].apply(lambda x: x if x >= 0 else column_mean)
    return df_in

def reverse_order(df_in):
    dic = {1.0 : 4.0, 2.0: 3.0, 3.0: 2.0, 4.0:1.0, 5.0: 0.0}
    for column in df_in.columns:
        vals = df_in[column].unique()
        if 1 in vals and 0 in vals:
            pass
        else:
            print column
            df_in[column] = df_in[column].replace(dic)
    return df_in


def pca_transform(df_in, num_components = None):
    if not num_components:
        num_components = df_in.shape[1]
    pca = PCA()
    df_out = pd.DataFrame(pca.fit_transform(df_in)).iloc[:,:num_components]
    return df_out,pca.explained_variance_, pca

def scree_plot(explained_variance):
    num_components = len(explained_variance)
    index = np.arange(num_components)
    labels = ['PC' + str(i) for i in xrange(1,num_components + 1)]
    plt.bar(index, explained_variance)
    bar_width = 0.35
    plt.xticks(index + bar_width,labels)

def regression(df,y_name,X_names):
    model = OLS(df[y_name],add_constant(df[X_names]))
    results = model.fit()
    return results

def regression_by_country(df,y_name,X_names):
    countries = df['S003'].unique()
    country_models = []
    for country in countries:
        df_by_country = df[df['S003'] == country]
        results = regression(df_by_country,y_name,X_names)
        country_models.append(results)
    return country_models

def regression_pca(df,y,X_indices):
    model = OLS(y,add_constant(df.iloc[:,X_indices]))
    results = model.fit()
    return results



if __name__ == '__main__':
    # create list of filenames, both for the integrated files and the raw files
    integrated_waves = ['WV1_integrated.csv', 'WV2_integrated.csv','WV3_integrated.csv','WV4_integrated.csv',
    'WV5_integrated.csv','WV6_integrated.csv']
    raw_waves = ['WV1.csv','WV2.csv','WV3.csv','WV4.csv','WV5.csv','WV6.csv']

    # append directory to filenames so they can be loaded
    integrated_wave_filenames = ['../Original_CSV_Files/integrated/' + wave for wave in integrated_waves]
    raw_wave_filenames = ['../Original_CSV_Files/raw/' + wave for wave in raw_waves]

    WVS_filename = '../WVS/Original_CSV_Files/integrated/longitudinal.csv'
    EVS_filename = '../EVS/ZA4804_v3-0-0.dta'


    df_WVS = load_csv(WVS_filename)
    df_EVS = load_stata(EVS_filename)
    df_total = pd.concat((df_WVS, df_EVS))
    df_total.reset_index(inplace = True)
    #columns = ['A001','A002','A003','A004','A005','A006','A007','A008','A009','S003','A032']
    columns = create_columns(40) + 'S003'
    df = choose_columns(df_total, columns )
    df_old = df.copy()
    df = reverse_order(df)
    df = remove_negatives(df)


    # regression analysis
    regression_columns = ['A001','A002','A003','A004','A005','A006','A007','A009']
    overall_results = regression(df,'A008',regression_columns)
    by_country_results = regression_by_country(df,'A008',regression_columns)

    ### for PCA
    df_no_country = df.drop(['S003','A008'],axis = 1)
    df_no_country2 = df.drop(['S003'],axis = 1)
    df_transformed, explained_variance, pca = pca_transform(df_no_country)
    df_transformed2, explained_variance2, pca2 = pca_transform(df_no_country2)
    # scree_plot(explained_variance)
    scree_plot(explained_variance2)
    pca_reg = regression_pca(df_transformed,df['A008'],[0,1,2,3,4,5,6])


    # df_transformed['country'] = df['S003']
    # group = df_transformed.groupby('country').mean()
    # plt.scatter(group.iloc[:,0], group.iloc[:,1])
    df_transformed2['country'] = df['S003']
    group2 = df_transformed2.groupby('country').mean()
    plt.scatter(group2.iloc[:,0], group2.iloc[:,1])
    plt.xlabel('PC1: Religion not important, politics not important ')
    plt.ylabel('PC2: Religion important, personal health low')

    # for column in df_original.columns:
    #     df_original[column] = df_original[column].apply(lambda x: x if type(x) is np.float64 else np.random.randn() )
    # start = time.clock()
    # pca.fit(df_original)
    # end = time.clock()
    # elapsed = end - start

    # scaler = StandardScaler()
    # k = KMeans(8)
    # dfs =load_waves()
    # #longitudinal = load_longitudinal()
    # pca = PCA()
    # dfs[5] = dfs[5].convert_objects(convert_numeric = True)
    # # dfs[5] = dfs[5].replace(-5,1)
    # # dfs[5] = dfs[5].replace(-4,1)
    # # dfs[5] = dfs[5].replace(-3,1)
    # # dfs[5] = dfs[5].replace(-2,1)
    # # dfs[5] = dfs[5].replace(-1,1)
    # for i in xrange(5,60):
    #     dfs[5].iloc[:,i] = dfs[5].iloc[:,i].replace(-5,2)
    #     dfs[5].iloc[:,i] = dfs[5].iloc[:,i].replace(-4,2)
    #     dfs[5].iloc[:,i] = dfs[5].iloc[:,i].replace(-3,2)
    #     dfs[5].iloc[:,i] = dfs[5].iloc[:,i].replace(-2,2)
    #     dfs[5].iloc[:,i] = dfs[5].iloc[:,i].replace(-1,2)
    # transformed = pca.fit_transform(dfs[5].iloc[:,5:10])
    # df_trans = pd.DataFrame(transformed)
    # df_trans['country'] = dfs[5].iloc[:,1]
    # group = df_trans.groupby('country').mean()
    # plt.scatter(group.iloc[:,0], group.iloc[:,1])
    # one = transformed[:,0]
    # one = scaler.fit_transform(one)
    # two = transformed[:,1]
    # two = scaler.fit_transform(two)
    # #two = 1000*two
    # both = np.vstack((one,two)).T
    # k.fit(both)
    # plt.scatter(two, one, c = k.labels_)
