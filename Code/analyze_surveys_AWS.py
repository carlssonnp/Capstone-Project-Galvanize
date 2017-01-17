import numpy as np
import pandas as pd
from sklearn.decomposition import PCA,NMF
from sklearn.preprocessing import MinMaxScaler, normalize
from sklearn.metrics.pairwise import euclidean_distances, cosine_distances
from scipy.stats import pearsonr, percentileofscore
import question_selector
from sklearn.cluster import KMeans
from country_dictionary import return_country_dictionary
import pickle
from time import time



class Entire_Survey():
    '''
    Class that contains the data for the 1981-2014 World and European Values Surveys. Creates DataFrame where each row is an individual, and the columns are questions from the survey.
    '''
    def __init__(self,autofit = True):
        '''
        INPUT:  Bool - whether or not to perform data cleaning upon loading of surveys

        Reads in WVS and EVS surveys; concatenates them together. Performs data cleaning if autofit is True.
        '''
        self.WVS_filename = 'https://s3.amazonaws.com/capstonebucket/longitudinal.csv'
        self.EVS_filename = 'https://s3.amazonaws.com/capstonebucket/ZA4804_v3-0-0.dta'
        self.WVS = pd.read_csv(self.WVS_filename).drop('Unnamed: 0', axis = 1)
        self.EVS = pd.read_stata(self.EVS_filename, convert_categoricals = False)
        self.fill_EVS_wave()
        self.combine_surveys()
        self.columns = []
        if autofit:
            self.fit()


    def fill_EVS_wave(self):
        '''
        Method that fills in the wave number for the EVS surveys; in the original data, they only have EVS wave number, which is not consistent chronologically with WVS wave number
        '''
        dic = {3:4, 4:5}
        self.EVS['S002'] = self.EVS['S002EVS'].replace(dic)

    def combine_surveys(self):
        '''
        Method that concatenates the World and European Surveys together.
        '''
        self.survey = pd.concat((self.WVS, self.EVS))
        self.survey.reset_index(inplace = True)
        self.survey.drop('index', axis = 1, inplace = True )

    def choose_columns_total(self):
        '''
        Chooses all questions from survey that are answered on a continous scale (i.e. 1-10, 1-4). Creates a DataFrame from 'survey' by including only these questions.
        '''
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

    # The following functions, create_columns_a - create_columns_i, determine what questions to use from each section

    def create_columns_a(self,num_vars = 222):
        '''
        INPUT: Int - number of variables to choose from section
        '''
        self.columns.extend(question_selector.create_columns_a(num_vars))
    def create_columns_b(self,num_vars = 23):
        '''
        INPUT: Int - number of variables to choose from section
        '''
        self.columns.extend(question_selector.create_columns_b(num_vars))
    def create_columns_c(self,num_vars = 64):
        '''
        INPUT: Int - number of variables to choose from section
        '''
        self.columns.extend(question_selector.create_columns_c(num_vars))
    def create_columns_d(self,num_vars = 80):
        '''
        INPUT: Int - number of variables to choose from section
        '''
        self.columns.extend(question_selector.create_columns_d(num_vars))
    def create_columns_e(self,num_vars = 267):
        '''
        INPUT: Int - number of variables to choose from section
        '''
        self.columns.extend(question_selector.create_columns_e(num_vars))
    def create_columns_f(self,num_vars = 205):
        '''
        INPUT: Int - number of variables to choose from section
        '''
        self.columns.extend(question_selector.create_columns_f(num_vars))
    def create_columns_g(self,num_vars = 51):
        '''
        INPUT: Int - number of variables to choose from section
        '''
        self.columns.extend(question_selector.create_columns_g(num_vars))
    def create_columns_h(self):
        '''
        INPUT: Int - number of variables to choose from section
        '''
        self.columns.extend(question_selector.create_columns_h())
    def create_columns_i(self):
        '''
        INPUT: Int - number of variables to choose from section
        '''
        self.columns.extend(question_selector.create_columns_i())

    def change_negative_to_nan(self):
        '''
        Changes all answers with negative values to NAN, as these are questions that were not answered. Creates a new DataFrame from 'survey_cleaned' to reflect this.
        '''
        self.survey_cleaned = self.survey_chosen_columns.copy()
        for column in self.survey_cleaned:
            self.survey_cleaned[column] = self.survey_cleaned[column].apply(lambda x: x if x>=0 else np.nan)

    def fit(self):
        '''
        Calls necessary functions to create the final cleaned DataFrame of the combined EVS and WVS file, with columns corresponding to the selected questions
        '''
        self.choose_columns_total()
        self.change_negative_to_nan()








class Wave():
    '''
    Class that contains the data for one particular time period of the survey. Creates DataFrame where each row is an individual, and the columns are questions from the survey. Also contains methods for dimensionality reduction to understand main drivers of variance in each time period.
    '''

    def __init__(self,wave_number,df_total,autofit = True):
        '''
        INPUT: INT - Time period with which to construct wave
               DATAFRAME - entire survey: World and European Values Surveys concatenated together
               BOOLEAN - whether or not to perform data cleaning and analysis upon instantiation of class

        Creates DataFrames corresponding to observations in the selected time period.
        '''
        self.wave_number = wave_number
        self.group_by_wave(df_total)
        if autofit:
            self.fit()

    def group_by_wave(self,df_total):
        '''
        Creates DataFrame from input survey by filtering out any observations that are not in the specified time period.
        '''
        self.survey = df_total[df_total['S002'] == self.wave_number].copy()



    def output_selected_questions(self,threshold):
        '''
        INPUT: FLOAT - minimum percent of question reponses that must not be NAN

        Calls 'keep_mostly_answered' function to only include survey questions that have percentage answered above the threshold value. Creates DataFrame from 'self.survey' by including only these questions.
        '''
        selected_questions =self.keep_mostly_answered(threshold)
        self.survey_selected_questions = self.survey[selected_questions].copy()

    def keep_mostly_answered(self,threshold):
        '''
        INPUT: FLOAT - minimum percent of question reponses that must not be NAN

        OUTPUT: LIST - a list of survey questions that have percentage answered above the threshold value
        '''
        question_percentage_answered = (self.survey.count()/self.survey.shape[0]).to_dict()
        mostly_answered = [key for key,value in question_percentage_answered.iteritems() if value > threshold]
        return sorted(mostly_answered)

    def drop_na(self):
        '''
        Creates DataFrame from 'survey_selected_questions' by dropping any row with an NAN value
        '''
        self.survey_delete_na = self.survey_selected_questions.dropna(axis = 0)



    def min_max_scale_questions(self):
        '''
        Function that min_max scales each feature/question to be in the range of 1-10. Since some of the questions are on a scale of 1-4, others range from 1-10, this could cause a problem with PCA since the method will likely pick up on the 1-10 questions more than the 1-4 questions (the former will likely have higher variance). Also note that I leave the identifying survey questions (country, year, wave) out, since these are not features I wish to transform.

        A new DataFrame is created from 'survey_delete_na' to reflect this scaling.
        '''
        scaler = MinMaxScaler(feature_range = (1,10))
        # scale up until the last 3 columns, which are identifying features and should not be transformed/included in the dimensionality reduction
        self.survey_scaled = pd.DataFrame(scaler.fit_transform(self.survey_delete_na.iloc[:,:-3]))
        self.survey_scaled.columns = self.survey_delete_na.columns[:-3]


    def pca_transform(self):
        '''
        Performs PCA on the cleaned survey data, and initializes class attributes to describe this transformation
        '''
        #sklearn pca object
        self.pca = PCA()
        #transformed data
        self.survey_in_PC_space = pd.DataFrame(self.pca.fit_transform(self.survey_scaled))
        self.survey_in_PC_space.columns = range(1,self.survey_in_PC_space.shape[1] + 1)
        self.survey_in_PC_space['country'] = self.survey_delete_na['S003'].copy().values

        # initializes V matrix, describing principal components as linear combinations of original survey questions. #Each row is a principal component, and each column is a survey question
        self.v_matrix = pd.DataFrame(self.pca.components_)
        self.v_matrix.columns = self.survey_scaled.columns
        self.v_matrix.index = range(1,self.v_matrix.shape[0] + 1)

        # contains explained_variance_ratio
        self.explained_variance_ratio = self.pca.explained_variance_ratio_

        # calls helper function to create dictionaries that hold information about the PCA transformation
        self.most_important_cols_pca()

        # creates DataFrame to contain both original question answers and principal component values for each respondent
        self.survey_question_and_PC = pd.concat((self.survey_scaled,self.survey_in_PC_space), axis = 1)

    #function that performs NMF on the cleaned survey data, and initializes a number of class attributes
    #that describe this transformation
    def nmf_transform(self,num_components):
        '''
        INPUT: INT - number of topics in the NMF decomposition

        Performs NMF on the cleaned survey data, and initializes class attributes to describe this transformation.
        '''
        # sklearn NMF object
        self.nmf = NMF(n_components = num_components)

        #transformed data
        self.survey_in_NMF_space = pd.DataFrame(self.nmf.fit_transform(self.survey_scaled))
        self.survey_in_NMF_space.columns = range(1,self.survey_in_NMF_space.shape[1] + 1)
        self.survey_in_NMF_space['country'] = self.survey_delete_na['S003'].copy().values

        #intializes H matrix, which describes each topic as a linear combination of the survey questions
        self.h_matrix = pd.DataFrame(self.nmf.components_)
        self.h_matrix.columns = self.survey_scaled.columns
        self.h_matrix.index = range(1,self.h_matrix.shape[0] + 1)

        # calls helper function to create dictionaries that hold information about the NMF transformation
        self.most_important_cols_nmf()
        #creates DataFrame that contains both the original survey answers and the NMF values for each respondent
        self.survey_question_and_NMF = pd.concat((self.survey_scaled,self.survey_in_NMF_space), axis = 1)


    def most_important_cols_pca(self):
        '''
        Creates class attributes that describe the makeup of the principal components in terms of the original survey questions.
        '''
        cols = self.v_matrix.columns

        #dictionary that contains principal component numbers as keys, with values being pandas Series containing the survey questions associated with that component in order of their association with that component
        self.component_dic_pca = {}
        for i in xrange(1,self.v_matrix.shape[0] + 1):
            feature_indices = np.argsort(np.abs(self.v_matrix.loc[i,:]))[::-1]
            features = cols[feature_indices]
            feature_values = self.v_matrix.loc[i,features]
            self.component_dic_pca[i] = pd.Series(index = features,data = feature_values)

        # matrix that contains correlations of questions with each principal component. The rows represent principal components, the columns represent survey questions .
        self.correlation_matrix_pca = self.v_matrix.copy()
        for column in self.survey_in_PC_space.columns[:-1]:
            for feature in self.survey_scaled:
                corr = pearsonr(self.survey_in_PC_space[column],self.survey_scaled[feature])
                self.correlation_matrix_pca.loc[column,feature] = corr[0]

        #dictionary that contains principal component numbers as keys, with values being pandas Series containing the survey questions associated with that component in order of their correlation with that component
        self.correlation_dic_pca ={}
        for i in xrange(1,self.correlation_matrix_pca.shape[0] + 1):
            feature_indices = np.argsort(np.abs(self.correlation_matrix_pca.loc[i,:]))[::-1]
            features = cols[feature_indices]
            feature_correlations = self.correlation_matrix_pca.loc[i,features]
            self.correlation_dic_pca[i] = pd.Series(index = features,data = feature_correlations)



    def most_important_cols_nmf(self):
        '''
        Creates class attributes that describe the makeup of the NMF topics in terms of the original survey questions.
        '''
        cols = self.h_matrix.columns

        #dictionary that contains NMF topics as keys, with values being pandas Series containing the survey questions associated with that topic in order of their association with that component
        self.component_dic_nmf = {}
        for i in xrange(1,self.h_matrix.shape[0] + 1):
            feature_indices = np.argsort(np.abs(self.h_matrix.loc[i,:]))[::-1]
            features = cols[feature_indices]
            feature_values = self.h_matrix.loc[i,features]
            self.component_dic_nmf[i] = pd.Series(index = features,data = feature_values)

        # matrix that contains correlations of questions with each NMF topic. The rows represent topics, the columns represent survey questions
        self.correlation_matrix_nmf = self.h_matrix.copy()
        for column in self.survey_in_NMF_space.columns[:-1]:
            for feature in self.survey_scaled:
                corr = pearsonr(self.survey_in_NMF_space[column],self.survey_scaled[feature])
                self.correlation_matrix_nmf.loc[column,feature] = corr[0]

        #dictionary that contains NMF topics as keys, with values being pandas Series containing the survey questions associated with that topic in order of their correlation with that component
        self.correlation_dic_nmf ={}
        for i in xrange(1,self.correlation_matrix_nmf.shape[0] + 1):
            feature_indices = np.argsort(np.abs(self.correlation_matrix_nmf.loc[i,:]))[::-1]
            features = cols[feature_indices]
            feature_correlations = self.correlation_matrix_nmf.loc[i,features]
            self.correlation_dic_nmf[i] = pd.Series(index = features,data = feature_correlations)





    def group_by_country(self):
        '''
        Groups both survey answers and derived features (PCA and NMF) by country, takes means
        '''
        self.grouped_by_country_pca = self.survey_question_and_PC.groupby('country').mean()
        self.grouped_by_country_nmf = self.survey_question_and_NMF.groupby('country').mean()

    def calculate_country_distances(self):
        '''
        Calculates euclidean distances of countries from one another based on per-country average survey responses
        '''
        length = self.grouped_by_country_pca.shape[1]
        # calculate distances based on first length/2 columns, since those columns contain answers to the original survey questions
        self.country_distances = pd.DataFrame(euclidean_distances(self.grouped_by_country_pca.iloc[:,:length/2]))
        self.country_distances.index = self.grouped_by_country_pca.index
        self.country_distances.columns =  self.grouped_by_country_pca.index

    def return_principal_component_questions(self,num_components,correlation_threshold):
        '''
        INPUT: INT - number of principal components to print out
               FLOAT - threshold above which correlations must be in order to be printed

        Prints out questions most correlated with principal components.
        '''
        for component_number in xrange(1,num_components + 1):
            component = self.correlation_dic_pca[component_number]
            print component[np.abs(component)>correlation_threshold]

    def return_nmf_questions(self,num_components,correlation_threshold):
        '''
        INPUT: INT - number of topics to print out
               FLOAT - threshold above which correlations must be in order to be printed

        Prints out questions most correlated with NMF topics.
        '''
        for component_number in xrange(1,num_components + 1):
            component = self.correlation_dic_nmf[component_number]
            print component[np.abs(component)>correlation_threshold]


    def calculate_percentiles(self,principal_component):
        '''
        INPUT: INT - principal component number to compare

        Calculates percentile of each country relative to other countries based on principal component score
        '''
        self.grouped_by_country_pca['pc'+str(principal_component) + '_percentile'] = [percentileofscore(-self.grouped_by_country_pca[principal_component],-i) for i in self.grouped_by_country_pca[principal_component]]

    def kmeans(self,cluster_number,num_components):
        '''
        INPUT: INT - number of clusters for k means
               INT - number of principle components to cluster on

        Performs k means clustering using the specified number of components
        '''
        #list containing sklearn k_means objects
        self.k_means = []
        # list containing lists of labels for countries after k means clustering
        self.labels = []
        for i in xrange(1,cluster_number + 1):
            kmeans = KMeans(i)
            kmeans.fit(self.grouped_by_country_pca[range(1,num_components+1)])
            self.k_means.append(kmeans)
            labels = kmeans.predict(self.grouped_by_country_pca[range(1,num_components+1)])
            self.labels.append(labels)


    def k_means_graph(self):
        '''
        Shows graph of inertia versus cluster number, to be used to determine the optimal cluster number.
        '''
        inertias = [cluster.inertia_ for cluster in self.k_means]
        plt.plot(xrange(1,len(self.k_means) + 1),inertias)
        plt.ylabel('Inertia')
        plt.xlabel('Cluster Number')
        plt.show()

    def pickle_correlation_dic(self):
        '''
        Pickles principal component-survey question correlation dictionaries, to be used with the flask web app
        '''
        with open('pickled_correlation_dictionaries/Wave' + str(self.wave_number) + '_correlation_dic.pkl','w') as f:
            pickle.dump(self.correlation_dic_pca,f)


    def output_graph_data(self,cluster_number,similarity_threshold):
        '''
        INPUT: INT - number of clusters to use when color shading country nodes
               FLOAT - threshold below which countries are considered to be connected

        Outputs node and edge files in csv format for use with Gephi; only produces edges between countries whose distance between countries is less than the threshold.
        '''
        edges = []
        counter = 0
        for source in self.country_distances.columns:
            for target in self.country_distances.index:
                if self.country_distances.loc[source,target] <similarity_threshold and source!=target:
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
        self.edges_out = edges_out

        nodes_out = pd.DataFrame(self.country_distances.index)
        nodes_out.columns = ['Id']
        nodes_out['Label'] = nodes_out['Id'].replace(return_country_dictionary())
        nodes_out['Kmeans'] = self.labels[cluster_number - 1]
        nodes_out.to_csv('Gephi_Files/Wave' + str(self.wave_number) + 'nodes.csv')
        self.nodes_out = nodes_out

    def fit(self):
        '''
        Calls all the necessary functions to create the final cleaned version of the wave file, rather than calling them each individually
        '''
        self.output_selected_questions(.7)
        self.drop_na()
        self.min_max_scale_questions()
        self.pca_transform()
        self.nmf_transform(4)
        self.group_by_country()
        self.calculate_country_distances()
        self.kmeans(7,4)
        self.calculate_percentiles(1)
        self.pickle_correlation_dic()



def plot_change():
    '''
    Plots change over time in the first principal component for the US, Russia, and Chile
    '''
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
    t1 = time()
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
    t2 = time()
    print t2 - t1

    # create plotly choropleth maps of first three principal components for each time period
    #plot_all_graphs(wave_list)

    # chart changes over time for first principal component in US, Russia, and Chile
    #plot_change()
