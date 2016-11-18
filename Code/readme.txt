This folder contains all of the files necessary to load, clean, and analyze the data. 

File descriptions: 

analyze_data2.py: A collection of functions used to perform analysis of the data. 

dict.txt: A text file mapping country codes to country names.

Wave*.html: These are html files that contain the plotly choropleth maps. I use them to create a local website using app.py, which I will later put online using the Heroku or Domino services. 

my_world.py: A file that uses the Plotly choropleth functionality to shade countries on the world map according the their average value
for a given feature (currently set up to display values of the first PCA component by country). 

read_data.py: File used to load in data. 

clean_data2.py: File used to clean data and select features for dimensionality reduction. 

wave_6_dict.py: File that used dict.txt to create a dictionary mapping country codes to country names. 

world.py: Template for Plotly choropleth functionality. 

app.py: File that sets up local server using Flask to display contents of html files. 

old_versions: a collection of old files that I used when first exploring the data. 
