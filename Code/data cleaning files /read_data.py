import pandas as pd

def load_csv(filename):
    df = pd.read_csv(filename)
    df.drop('Unnamed: 0', axis = 1, inplace = True)
    return df

def load_stata(filename):
    df = pd.read_stata(filename, convert_categoricals = False)
    return df


if __name__ == '__main__':
    df = load_wave('enter filename here')
