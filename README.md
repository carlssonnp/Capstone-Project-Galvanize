# Capstone-Project
Galvanize Cohort 18 - Capstone Project

In this project, I use data from the World Values Survey and European Values Survey to track social values across time and space: space, because the surveys cover over 100 countries across the globe, and time, because the surveys are cross sectional, covering the years 1981 through 2014. Each survey contains hundreds of questions on a diverse set of topics, including politics, family, economics, religion, and more. While the surveys hold great potential for comparison between countries and time periods, the sheer volume of questions makes it difficult to make comparisons between countries (space) and survey period (time) on a question by question basis. I hope to make this comparison easier by reducing the dimensionality of the survey using Principal Component Analysis (PCA), finding overarching themes that are explained by clusters of questions, and then presenting the results in pictorial format via a Flask app.  

Quick description of folders:

Code: contains all of the code necessary for the project, including:

- the data loading/analysis file : analyze_surveys.py
- a text file mapping numerical country codes to country names: country_codes.txt
- a file that creates a python dictionary mapping numerical country codes to country names: country_dictionary.py
- a file that determines what questions to select from the surveys: question_selector.py
- the Plotly mapping file: plotly_choropleth.py
- the Flask web app file: app.py
- html/css files for use with the app file: html_files folder and static folder, respectively
- Gephi graph files: Gephi_Files
- pickled dictionaries of principal component values for use with the app file: pickled_correlation_dictionaries.py
- the codebook for identifying survey questions: codebook.csv
- a list my interpretations of the principal components for each time period: principal_components_list.md


EVS: Folder than contains data files on my machine. Due to size constraints, no data will be uploaded to Github. On Github, this folder only contains the data dictionary. Anyone interested in taking a look at the survey data themselves can use the following link:
http://www.europeanvaluesstudy.eu/

WVS: Folder than contains data files on my machine. Due to size constraints, no data will be uploaded to Github. On Github, this folder only contains the data dictionary. Anyone interested in taking a look at the survey data themselves can use the following link:
http://www.worldvaluessurvey.org/wvs.jsp

Presentation Materials: a keynote presentation of my results, as well as the associated images
