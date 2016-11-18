from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler,MinMaxScaler
from sklearn.cluster import KMeans, DBSCAN
import numpy as np
from read_data import load_csv, load_stata
import pandas as pd
from statsmodels.regression.linear_model import OLS, WLS
from statsmodels.api import add_constant
from clean_data import *

# def count_missing(df_old):
#     df_out = df_old.copy()
#     missing = []
#     for column in df_out:
#         df_out[column].fillna(-10)
#         missing.append(sum(df_out[column] < 0))
#     return missing, df_out





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

    # load longitudinal data
    df_WVS = load_csv(WVS_filename)
    df_EVS = load_stata(EVS_filename)
    #fill in EVS wave variable
    df_EVS = fill_wave(df_EVS)
    # append data frames
    df_total = pd.concat((df_WVS, df_EVS))
    #reset index
    df_total.reset_index(inplace = True)
    # create A variable columns; S003 is country, S002 is wave, S020 is year
    columns = create_columns(222) + ['S003'] + ['S002'] + ['S020']
    df = choose_columns(df_total, columns )


    df = reverse_order(df)
    df_old = df.copy()
    df = change_to_nan(df)
    #df = get_dummies(df,['A044','A045','A050','A169','A174'])
    #df = remove_negatives(df)
    ##### TEMPORARY
    df1 = group_by_wave(1,df)
    df2 = group_by_wave(2,df)
    df3 = group_by_wave(3,df)
    df4 = group_by_wave(4,df)
    df5 = group_by_wave(5,df)
    df6 = group_by_wave(6,df)

    df1_final = output_cleaned_df(df1)
    df2_final = output_cleaned_df(df2)
    df3_final = output_cleaned_df(df3)
    df4_final = output_cleaned_df(df4)
    df5_final = output_cleaned_df(df5)
    df6_final = output_cleaned_df(df6)
    df_final = output_cleaned_df(df)

    df1_for_transform = df1_final.dropna(axis = 0)
    df2_for_transform = df2_final.dropna(axis = 0)
    df3_for_transform = df3_final.dropna(axis = 0)
    df4_for_transform = df4_final.dropna(axis = 0)
    df5_for_transform = df5_final.dropna(axis = 0)
    df6_for_transform = df6_final.dropna(axis = 0)


    df_for_transform = df[for_transform]
    df_for_transform = get_dummies(df_for_transform)
    df_for_transform = df_for_transform.dropna(axis = 0)
    from sklearn.preprocessing import StandardScaler
    scaler = StandardScaler(with_std = False)
    df_test = scaler.fit_transform(df6_for_transform)
    scaler = MinMaxScaler(feature_range=(0, 10))
    df6 = df6_for_transform.apply(lambda x: MinMaxScaler(feature_range = (1,10)).fit_transform(x))
    df_transformed, explained_variance, pca = pca_transform(df6.iloc[:,1:10] )
    # regression analysis
    # regression_columns = ['A001','A002','A003','A004','A005','A006','A007','A009']
    # regression_columns = list(df.columns)
    # regression_columns.remove('S003')
    # regression_columns.remove('A008')
    print most_important_cols(pca.components_,df6_for_transform)

    overall_results = regression(df,'A008',regression_columns)
    by_country_results = regression_by_country(df,'A008',regression_columns)

    ### for PCA
    df_no_country = df.drop(['S003','A008'],axis = 1)
    df_no_country2 = df.drop(['S003'],axis = 1)
    df_transformed, explained_variance, pca = pca_transform(df_no_country)
    df_transformed2, explained_variance2, pca2 = pca_transform(df_no_country2)
    # scree_plot(explained_variance)
    #scree_plot(explained_variance2[:10])
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
