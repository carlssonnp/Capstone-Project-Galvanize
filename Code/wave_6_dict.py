

with open('dict.txt','r') as f:
    country_list = []
    for l in f:
        country_list = l.split('\r')
    country_list2 = []
    for l in country_list[:-7]:
        country_3 = []
        split = l.split('##')
        country_3.append(split[0])
        country_3.append(split[1])
        country_list2.append(country_3)

    d = {}
    for country in country_list2:
        d[country[0]] = country[1]

    int_dic = {int(key): item for key, item in d.iteritems() }
