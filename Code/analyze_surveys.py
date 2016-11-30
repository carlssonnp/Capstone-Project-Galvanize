import numpy as np
import pandas as pd
from sklearn.decomposition import PCA,NMF
from sklearn.preprocessing import MinMaxScaler, normalize
from sklearn.metrics.pairwise import euclidean_distances, cosine_distances
from scipy.stats import pearsonr, percentileofscore
from plotly_choropleth import plot_choropleth, plot_all_graphs
import question_selector
from sklearn.cluster import KMeans
from country_dictionary import country_dictionary
import pickle
import matplotlib.pyplot as plt


class Entire_Survey():
    #reads in WVS and EVS surveys; concatenates them together
    def __init__(self,autofit = True):
        self.WVS_filename = '../WVS/Original_CSV_Files/integrated/longitudinal.csv'
        self.EVS_filename = '../EVS/ZA4804_v3-0-0.dta'
        self.WVS = pd.read_csv(self.WVS_filename).drop('Unnamed: 0', axis = 1)
        self.EVS = pd.read_stata(self.EVS_filename, convert_categoricals = False)
        self.fill_EVS_wave()
        self.combine_surveys()
        self.columns = []
        if autofit:
            self.fit()

    # method that fills in the wave number for the EVS surveys; they only have EVS wave number, which is not
    # consistent chronologically with WVS wave number
    def fill_EVS_wave(self):
        dic = {3:4, 4:5}
        self.EVS['S002'] = self.EVS['S002EVS'].replace(dic)

    #combines WVS and EVS surveys
    def combine_surveys(self):
        self.survey = pd.concat((self.WVS, self.EVS))
        self.survey.reset_index(inplace = True)
        self.survey.drop('index', axis = 1, inplace = True )

    # chooses all questions from survey that are answered on a continous scale (i.e. 1-10, 1-4)
    def choose_columns_total(self):
            self.create_columns_a()
            self.create_columns_b()
            self.create_columns_c()
            self.create_columns_d()
            self.create_columns_e()
            self.create_columns_f()
            self.create_columns_g()
            self.create_columns_h()
            self.create_columns_i()

            #add in the identifying columns: S003 (country), S002 (wave number), S020 (year of survey)
            self.columns +=  ['S003'] + ['S002'] + ['S020']
            self.survey_chosen_columns = self.survey[self.columns].copy()

    # the following functions, create_columns_a - create_columns_i, determine what questions to use from each section
    def create_columns_a(self,num_vars = 222):
        self.columns.extend(question_selector.create_columns_a(num_vars))
    def create_columns_b(self,num_vars = 23):
        self.columns.extend(question_selector.create_columns_b(num_vars))
    def create_columns_c(self,num_vars = 64):
        self.columns.extend(question_selector.create_columns_c(num_vars))
    def create_columns_d(self,num_vars = 80):
        self.columns.extend(question_selector.create_columns_d(num_vars))
    def create_columns_e(self,num_vars = 267):
        self.columns.extend(question_selector.create_columns_e(num_vars))
    def create_columns_f(self,num_vars = 205):
        self.columns.extend(question_selector.create_columns_f(num_vars))
    def create_columns_g(self,num_vars = 51):
        self.columns.extend(question_selector.create_columns_g(num_vars))
    def create_columns_h(self):
        self.columns.extend(question_selector.create_columns_h())
    def create_columns_i(self):
        self.columns.extend(question_selector.create_columns_i())

    #this method changes all answers with negative values to NAN, as these are questions that were not answered.
    def change_negative_to_nan(self):
        self.survey_cleaned = self.survey_chosen_columns.copy()
        for column in self.survey_cleaned:
            self.survey_cleaned[column] = self.survey_cleaned[column].apply(lambda x: x if x>=0 else np.nan)
    # this method calls all the necessary functions to create the final cleaned version of the combined EVS and WVS
    # file, rather than calling them each individually
    def fit(self):
        self.choose_columns_total()
        self.change_negative_to_nan()








class Wave():
    #initializes wave class, containing the data for one wave
    def __init__(self,wave_number,df_total,autofit = True):
        self.wave_number = wave_number
        self.group_by_wave(df_total)
        if autofit:
            self.fit()

    # function that keeps only the observations that are part of the specified wave
    def group_by_wave(self,df_in):
        self.survey = df_in[df_in['S002'] == self.wave_number].copy()


    # function that sorts the output columns of the 'keep_answered' function and removes columns for wave number,
    #country, and year, since these columns represent identifying variables and should not be used in the PCA
    #analysis
    def output_selected_questions(self,threshold):
        selected_questions =self.keep_mostly_answered(threshold)
        self.survey_selected_questions = self.survey[selected_questions].copy()

    # function that determines which columns to keep, based on an input threshold that represents minimum percent
    # of data that must not be missing
    def keep_mostly_answered(self,threshold):
        question_percentage_answered = (self.survey.count()/self.survey.shape[0]).to_dict()
        mostly_answered = [key for key,value in question_percentage_answered.iteritems() if value > threshold]
        return sorted(mostly_answered)


    #function that drops any row with an NAN value; will look into better ways to deal with missing values later
    def drop_na(self):
        self.survey_delete_na = self.survey_selected_questions.dropna(axis = 0)


    # function that min_max scales each feature/question to be in the range of 1-10. Since some of the questions are on
    #a scale of 1-4, others range from 1-10, this could cause a problem with PCA since the method will likely pick up on
    #the 1-10 questions more than the 1-4 questions (the former will likely have higher variance). Also note that
    # I leave the identifying survey questions (country, year, wave) out, since these are not features I wish to
    # transform
    def min_max_scale_questions(self):
        scaler = MinMaxScaler(feature_range = (1,10))
        self.survey_scaled = pd.DataFrame(scaler.fit_transform(self.survey_delete_na.iloc[:,:-3]))
        self.survey_scaled.columns = self.survey_delete_na.columns[:-3]


    #function that performs PCA on the cleaned survey data, and initializes a number of class attributes
    #that describe this transformation
    def pca_transform(self):
        self.pca = PCA()
        self.survey_in_PC_space = pd.DataFrame(self.pca.fit_transform(self.survey_scaled))
        self.survey_in_PC_space.columns = range(1,self.survey_in_PC_space.shape[1] + 1)
        self.survey_in_PC_space['country'] = self.survey_delete_na['S003'].copy().values

        self.v_matrix = pd.DataFrame(self.pca.components_)
        self.v_matrix.columns = self.survey_scaled.columns
        self.v_matrix.index = range(1,self.v_matrix.shape[0] + 1)
        self.explained_variance = self.pca.explained_variance_

        self.most_important_cols_pca()
        self.survey_question_and_PC = pd.concat((self.survey_scaled,self.survey_in_PC_space), axis = 1)

    #function that performs NMF on the cleaned survey data, and initializes a number of class attributes
    #that describe this transformation
    def nmf_transform(self,num_components):
        self.nmf = NMF(n_components = num_components)
        self.survey_in_NMF_space = pd.DataFrame(self.nmf.fit_transform(self.survey_scaled))
        self.survey_in_NMF_space.columns = range(1,self.survey_in_NMF_space.shape[1] + 1)
        self.survey_in_NMF_space['country'] = self.survey_delete_na['S003'].copy().values

        self.h_matrix = pd.DataFrame(self.nmf.components_)
        self.h_matrix.columns = self.survey_scaled.columns
        self.h_matrix.index = range(1,self.h_matrix.shape[0] + 1)
        self.most_important_cols_nmf()
        self.survey_question_and_NMF = pd.concat((self.survey_scaled,self.survey_in_NMF_space), axis = 1)


    # function that initializes variables that describe the makeup of each principal component in terms of the
    # original survey questions
    def most_important_cols_pca(self):
        cols = self.v_matrix.columns
        self.component_dic_pca = {}
        self.correlation_matrix_pca = self.v_matrix.copy()
        self.correlation_dic_pca ={}

        for i in xrange(1,self.v_matrix.shape[0] + 1):
            feature_indices = np.argsort(np.abs(self.v_matrix.loc[i,:]))[::-1]
            features = cols[feature_indices]
            feature_values = self.v_matrix.loc[i,features]
            self.component_dic_pca[i] = pd.Series(index = features,data = feature_values)

        for column in self.survey_in_PC_space.columns[:-1]:
            for feature in self.survey_scaled:
                corr = pearsonr(self.survey_in_PC_space[column],self.survey_scaled[feature])
                self.correlation_matrix_pca.loc[column,feature] = corr[0]

        for i in xrange(1,self.correlation_matrix_pca.shape[0] + 1):
            feature_indices = np.argsort(np.abs(self.correlation_matrix_pca.loc[i,:]))[::-1]
            features = cols[feature_indices]
            feature_correlations = self.correlation_matrix_pca.loc[i,features]
            self.correlation_dic_pca[i] = pd.Series(index = features,data = feature_correlations)

    # function that initializes variables that describe the makeup of each NMF topic in terms of the
    # original survey questions
    def most_important_cols_nmf(self):
        cols = self.h_matrix.columns
        self.component_dic_nmf = {}
        self.correlation_matrix_nmf = self.h_matrix.copy()
        self.correlation_dic_nmf ={}

        for i in xrange(1,self.h_matrix.shape[0] + 1):
            feature_indices = np.argsort(np.abs(self.h_matrix.loc[i,:]))[::-1]
            features = cols[feature_indices]
            feature_values = self.h_matrix.loc[i,features]
            self.component_dic_nmf[i] = pd.Series(index = features,data = feature_values)

        for column in self.survey_in_NMF_space.columns[:-1]:
            for feature in self.survey_scaled:
                corr = pearsonr(self.survey_in_NMF_space[column],self.survey_scaled[feature])
                self.correlation_matrix_nmf.loc[column,feature] = corr[0]

        for i in xrange(1,self.correlation_matrix_nmf.shape[0] + 1):
            feature_indices = np.argsort(np.abs(self.correlation_matrix_nmf.loc[i,:]))[::-1]
            features = cols[feature_indices]
            feature_correlations = self.correlation_matrix_nmf.loc[i,features]
            self.correlation_dic_nmf[i] = pd.Series(index = features,data = feature_correlations)


    # function that groups suvey questions and derived features (PCA and NMF) by country and takes the mean of these
    #columns
    def group_by_country(self):
        self.grouped_by_country_pca = self.survey_question_and_PC.groupby('country').mean()
        self.grouped_by_country_nmf = self.survey_question_and_NMF.groupby('country').mean()

    # function that calculates euclidean distances of countries from one another based on per-country average
    # survey responses
    def calculate_country_distances(self):
        length = self.grouped_by_country_pca.shape[1]
        self.country_distances = pd.DataFrame(euclidean_distances(self.grouped_by_country_pca.iloc[:,:length/2]))
        self.country_distances.index = self.grouped_by_country_pca.index
        self.country_distances.columns =  self.grouped_by_country_pca.index

    # function that prints the questions most correlated with a particular principal component
    def return_principal_component_questions(self,num_components,correlation_threshold):
        for component_number in xrange(1,num_components + 1):
            component = self.correlation_dic_pca[component_number]
            print component[np.abs(component)>correlation_threshold]
    # function that prints the questions most correlated with a particular NMF topic
    def return_nmf_questions(self,num_components,correlation_threshold):
        for component_number in xrange(1,num_components + 1):
            component = self.correlation_dic_nmf[component_number]
            print component[np.abs(component)>correlation_threshold]

    # function that calculates the percentile of a country's values for the first principal component relative to
    # the other countries
    def calculate_percentiles(self):
        self.grouped_by_country_pca['pc1_percentile'] = [percentileofscore(-self.grouped_by_country_pca[1],-i) for i in self.grouped_by_country_pca[1]]

    # function that performs k means clustering on the first 4 principal components
    def kmeans(self,cluster_number):
        self.k_means = []
        self.labels = []
        for i in xrange(cluster_number):
            kmeans = KMeans(i + 1)
            kmeans.fit(self.grouped_by_country_pca[[1,2,3,4]])
            self.k_means.append(kmeans)
            labels = kmeans.predict(self.grouped_by_country_pca[[1,2,3,4]])
            self.labels.append(labels)
        self.grouped_by_country_pca['labels'] = self.labels[2]

    # function that shows a graph of inertia versus cluster number to be used to determine that optimal cluster number
    def k_means_graph(self):
        inertias = [cluster.inertia_ for cluster in self.k_means]
        plt.plot(xrange(1,len(self.k_means) + 1),inertias)
        plt.show()

    # function that pickles the PCA component - survey question correlation dictionaries to be used with the
    # flask web app
    def pickle_correlation_dic(self):
        with open('pickled_correlation_dictionaries/Wave' + str(self.wave_number) + '_correlation_dic.pkl','w') as f:
            pickle.dump(self.correlation_dic_pca,f)


    # function that outputs node and edge files in csv format for use with Gephi; only produces edges between
    # countries whose distance between surveys is less than 6
    def output_graph_data(self,cluster_number):
        edges = []
        counter = 0
        for source in self.country_distances.columns:
            for target in self.country_distances.index:
                if self.country_distances.loc[source,target] <6 and source!=target:
                    edges_row = []
                    similarity = 1./self.country_distances.loc[source,target]
                    edges_row.append(source)
                    edges_row.append(target)
                    edges_row.append('Undirected')
                    edges_row.append(counter)
                    edges_row.append(similarity)
                    edges_row.append(1)
                    counter+=1
                    edges.append(edges_row)
        edges = np.array(edges)
        edges_out = pd.DataFrame(edges)
        edges_out.columns = ['Source','Target','Type', 'Id', 'Weight', 'Average Degree']
        edges_out.to_csv('Gephi_Files/Wave' + str(self.wave_number) + 'edges.csv')

        nodes_out = pd.DataFrame(self.country_distances.index)
        nodes_out.columns = ['Id']
        nodes_out['Label'] = nodes_out['Id'].replace(country_dictionary)
        nodes_out['Label'] = nodes_out['Label'].replace({499:'Montenegro', 688: 'Serbia'})
        nodes_out['Kmeans'] = self.labels[cluster_number + 1]
        nodes_out.to_csv('Gephi_Files/Wave' + str(self.wave_number) + 'nodes.csv')


    # this method calls all the necessary functions to create the final cleaned version of the wave
    # file, rather than calling them each individually
    def fit(self):
        self.output_selected_questions(.7)
        self.drop_na()
        self.min_max_scale_questions()
        self.pca_transform()
        self.nmf_transform(4)
        self.group_by_country()
        self.calculate_country_distances()
        self.pickle_correlation_dic()
        self.kmeans(7)
        self.calculate_percentiles()



# function that plots the change over time in the first principal component for the US, Russia, and Chile
def plot_change():
    wv1 = Wave1.grouped_by_country_pca['pc1_percentile']
    wv2 = Wave2.grouped_by_country_pca['pc1_percentile']
    wv3 = Wave3.grouped_by_country_pca['pc1_percentile']
    wv4 = Wave4.grouped_by_country_pca['pc1_percentile']
    wv5 = Wave5.grouped_by_country_pca['pc1_percentile']
    wv6 = Wave6.grouped_by_country_pca['pc1_percentile']

    US = pd.Series([wv2[840],wv3[840],wv4[840],wv5[840]])
    Chile = pd.Series([wv2[152],wv3[152],wv4[152],wv5[152]])
    Russia = pd.Series([wv2[643],wv3[643],wv5[643]])
    US_x = [1994,1998,2004,2009]
    Chile_x = [1994,1998,2004,2009]
    Russia_x = [1994,1998,2009]

    plot1, = plt.plot(US_x,US)
    plot2, = plt.plot(Chile_x,Chile)
    plot3, = plt.plot(Russia_x,Russia)
    plt.legend([plot1,plot2,plot3],["US", "Chile",'Russia'])
    plt.xlabel('Year')
    plt.ylabel('Percentile of liberal social values/secularism component')
    plt.show()



if __name__ == '__main__':
    # create main survey
    survey = Entire_Survey()
    # stratify by time period
    Wave1 = Wave(1,survey.survey_cleaned)
    Wave2 = Wave(2,survey.survey_cleaned)
    Wave3 = Wave(3,survey.survey_cleaned)
    Wave4 = Wave(4,survey.survey_cleaned)
    Wave5 = Wave(5,survey.survey_cleaned)
    Wave6 = Wave(6,survey.survey_cleaned)
    wave_list = [Wave1, Wave2, Wave3, Wave4, Wave5, Wave6]
    # create plotly choropleth maps of first three principal components for each time period
    plot_all_graphs(wave_list)
    # chart changes over time for first principal component in US, Russia, and Chile
    plot_change()
