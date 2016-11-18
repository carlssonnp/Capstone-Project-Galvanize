import pandas as pd

def showmissing_EVS(df):
    missing = []
    for column in df:
        missing.append(df[column].count())
    return missing 
