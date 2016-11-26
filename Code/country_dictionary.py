

with open('country_codes.txt','r') as f:
    countries = []
    countries = f.read().split('\r')

    countries_id_to_name = []
    for country in country_list[:-6]:
        id_name_split = country.split('##')
        countries_id_to_name.append(id_name_split)

    country_dictionary = {}
    for country in countries_id_to_name:
        country_dictionary[country[0]] = country[1]

    country_dictionary = {int(key): item for key, item in country_dictionary.iteritems() }
