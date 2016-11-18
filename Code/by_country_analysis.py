def pc_by_country(df):
    group = df.groupby('country').mean().iloc[:,0]
    return group
