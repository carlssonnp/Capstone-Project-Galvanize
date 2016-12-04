def return_country_dictionary():
     '''
     OUTPUT: dictionary with country codes as keys and country names as values

     Creates a dictionary mapping country codes (numeric) to country names (values)
     '''
     with open('country_codes.txt','r') as f:
         countries = f.read().split('\r')

         #The last six lines of the country name file are not countries
         countries_id_to_name = [country.split('##') for country in countries[:-6]]

         country_dictionary = {int(country[0]): country[1] for country in countries_id_to_name}

         return country_dictionary
