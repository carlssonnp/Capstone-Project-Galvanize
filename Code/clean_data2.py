### fill in the wave number for the EVS
import numpy as np
def fill_wave(df_in):
    df_out = df_in.copy()
    dic = {3:4, 4:5}
    df_out['S002'] = df_in['S002EVS'].replace(dic)
    return df_out

def create_columns_a_original(num_vars):
    col_nums = xrange(1,num_vars + 1)
    columns = []
    for col_num in col_nums:
        if col_num < 10:
            columns.append('A00' + str(col_num))
        elif col_num <100:
            columns.append('A0' + str(col_num))
        else:
            columns.append('A' + str(col_num))
    bad_cols = []
    for col_num in range(124,165):
        bad_cols.append('A' + str(col_num))
    for col_num in range(175,189):
        bad_cols.append('A' + str(col_num))
    good_cols = set(columns) - set(bad_cols)
    return sorted(list(good_cols))

def create_columns_a(num_vars):
    col_nums = xrange(1,num_vars + 1)
    columns = []
    for col_num in col_nums:
        if col_num < 10:
            columns.append('A00' + str(col_num))
        elif col_num <100:
            columns.append('A0' + str(col_num))
        else:
            columns.append('A' + str(col_num))
    bad_cols = []
    for col_num in range(10,20):
        bad_cols.append('A0' + str(col_num))
    for col_num in range(25,57):
        bad_cols.append('A0' + str(col_num))
    for col_num in range(64,100):
        bad_cols.append('A0' + str(col_num))
    for col_num in range(100,107):
        bad_cols.append('A' + str(col_num))
    for col_num in range(123,166):
        bad_cols.append('A' + str(col_num))
    for col_num in range(168,170):
        bad_cols.append('A' + str(col_num))
    for col_num in range(174,200):
        bad_cols.append('A' + str(col_num))
    for col_num in range(208,213):
        bad_cols.append('A' + str(col_num))
    good_cols = set(columns) - set(bad_cols)
    return sorted(list(good_cols))

def create_columns_b(num_vars):
    col_nums = xrange(1,num_vars + 1)
    columns = []
    for col_num in col_nums:
        if col_num < 10:
            columns.append('B00' + str(col_num))
        elif col_num <100:
            columns.append('B0' + str(col_num))
        else:
            columns.append('B' + str(col_num))
    bad_cols = []
    for col_num in range(8,10):
        bad_cols.append('B00' + str(col_num))
    for col_num in range(10,18):
        bad_cols.append('B0' + str(col_num))
    good_cols = set(columns) - set(bad_cols)
    return sorted(list(good_cols))


def create_columns_c(num_vars):
    col_nums = xrange(1,num_vars + 1)
    columns = []
    for col_num in col_nums:
        if col_num < 10:
            columns.append('C00' + str(col_num))
        elif col_num <100:
            columns.append('C0' + str(col_num))
        else:
            columns.append('C' + str(col_num))
    bad_cols = []
    for col_num in range(1,6):
        bad_cols.append('C00' + str(col_num))
    bad_cols.append('C009')
    for col_num in range(10,31):
        bad_cols.append('C0' + str(col_num))
    for col_num in range(42,62):
        bad_cols.append('C0' + str(col_num))
    good_cols = set(columns) - set(bad_cols)
    return sorted(list(good_cols))

def create_columns_d(num_vars):
    col_nums = xrange(1,num_vars + 1)
    columns = []
    for col_num in col_nums:
        if col_num < 10:
            columns.append('D00' + str(col_num))
        elif col_num <100:
            columns.append('D0' + str(col_num))
        else:
            columns.append('D' + str(col_num))
    bad_cols = []
    for col_num in range(3,10):
        bad_cols.append('D00' + str(col_num))
    for col_num in range(10,20):
        bad_cols.append('D0' + str(col_num))
    for col_num in range(21,26):
        bad_cols.append('D0' + str(col_num))
    for col_num in range(44,54):
        bad_cols.append('D0' + str(col_num))
    good_cols = set(columns) - set(bad_cols)
    return sorted(list(good_cols))

def create_columns_e(num_vars):
    col_nums = xrange(1,num_vars + 1)
    columns = []
    for col_num in col_nums:
        if col_num < 10:
            columns.append('E00' + str(col_num))
        elif col_num <100:
            columns.append('E0' + str(col_num))
        else:
            columns.append('E' + str(col_num))
    bad_cols = []
    for col_num in range(1,7):
        bad_cols.append('E00' + str(col_num))
    for col_num in range(11,13):
        bad_cols.append('E0' + str(col_num))
    for col_num in range(14,21):
        bad_cols.append('E0' + str(col_num))
    bad_cols.append('E022')
    for col_num in range(25,33):
        bad_cols.append('E0' + str(col_num))
    for col_num in range(48,57):
        bad_cols.append('E0' + str(col_num))
    for col_num in range(48,57):
        bad_cols.append('E0' + str(col_num))
    bad_cols.append('E062')
    for col_num in range(118,120):
        bad_cols.append('E' + str(col_num))
    for col_num in range(126,130):
        bad_cols.append('E' + str(col_num))
    for col_num in range(131,133):
        bad_cols.append('E' + str(col_num))
    for col_num in range(135,140):
        bad_cols.append('E' + str(col_num))
    for col_num in range(144,146):
        bad_cols.append('E' + str(col_num))
    for col_num in range(178,184):
        bad_cols.append('E' + str(col_num))
        bad_cols.append('E187')
    for col_num in range(190,196):
        bad_cols.append('E' + str(col_num))
    for col_num in range(190,196):
        bad_cols.append('E' + str(col_num))
    bad_cols.append('E197')
    for col_num in range(199,203):
        bad_cols.append('E' + str(col_num))
    for col_num in range(199,203):
        bad_cols.append('E' + str(col_num))
    bad_cols.append('E204')
    bad_cols.append('E206')
    for col_num in range(209,212):
        bad_cols.append('E' + str(col_num))
    for col_num in range(213,220):
        bad_cols.append('E' + str(col_num))
    for col_num in range(221,224):
        bad_cols.append('E' + str(col_num))
    for col_num in range(237,242):
        bad_cols.append('E' + str(col_num))
    for col_num in range(248,255):
        bad_cols.append('E' + str(col_num))
    for col_num in range(256,263):
        bad_cols.append('E' + str(col_num))
    bad_cols.append('E265')
    good_cols = set(columns) - set(bad_cols)
    return sorted(list(good_cols))


def create_columns_f(num_vars):
    col_nums = xrange(1,num_vars + 1)
    columns = []
    for col_num in col_nums:
        if col_num < 10:
            columns.append('F00' + str(col_num))
        elif col_num <100:
            columns.append('F0' + str(col_num))
        else:
            columns.append('F' + str(col_num))
    bad_cols = []
    bad_cols.append('F011')
    for col_num in range(13,28):
        bad_cols.append('F0' + str(col_num))
    bad_cols.append('F029')
    for col_num in range(31,34):
        bad_cols.append('F0' + str(col_num))
    bad_cols.append('F062')
    for col_num in range(35,61):
        bad_cols.append('F0' + str(col_num))
    for col_num in range(64,66):
        bad_cols.append('F0' + str(col_num))
    for col_num in range(88,93):
        bad_cols.append('F0' + str(col_num))
    bad_cols.append('F098')
    for col_num in range(176,186):
        bad_cols.append('F' + str(col_num))
    for col_num in range(188,190):
        bad_cols.append('F' + str(col_num))
    bad_cols.append('F192')
    for col_num in range(200,202):
        bad_cols.append('F' + str(col_num))

    good_cols = set(columns) - set(bad_cols)
    return sorted(list(good_cols))

def create_columns_g(num_vars):
    col_nums = xrange(1,num_vars + 1)
    columns = []
    for col_num in col_nums:
        if col_num < 10:
            columns.append('G00' + str(col_num))
        elif col_num <100:
            columns.append('G0' + str(col_num))
        else:
            columns.append('G' + str(col_num))
    bad_cols = []
    for col_num in range(4,6):
        bad_cols.append('G00' + str(col_num))
    for col_num in range(7,10):
        bad_cols.append('G00' + str(col_num))
    for col_num in range(10,14):
        bad_cols.append('G0' + str(col_num))
    for col_num in range(15,19):
        bad_cols.append('G0' + str(col_num))
    bad_cols.append('G022')
    for col_num in range(24,28):
        bad_cols.append('G0' + str(col_num))
    good_cols = set(columns) - set(bad_cols)
    return sorted(list(good_cols))

def create_columns_h():
    return ['H001']

def create_columns_i():
    return ['I001', 'I002']


def choose_columns(df_in,columns):
    df_out = df_in.ix[:,columns]
    return df_out



def reverse_order(df_in):
    dic = {1.0 : 4.0, 2.0: 3.0, 3.0: 2.0, 4.0:1.0, 5.0: 0.0, 6.0:-1.0}
    already_reversed_columns1 = ['A' + str(var_num) for var_num in xrange(107,121)]
    already_reversed_columns2 = ['A' + str(var_num) for var_num in xrange(166,168)]
    already_reversed_columns3 = ['A' + str(var_num) for var_num in xrange(170,174)]
    already_reversed_columns4 = ['A' + str(var_num) for var_num in xrange(200,208)]
    already_reversed_columns5 = ['A' + str(var_num) for var_num in xrange(213,223)]
    total_reversed_columns = already_reversed_columns1 + already_reversed_columns2 + already_reversed_columns3 + already_reversed_columns4 + already_reversed_columns5
    total_reversed_columns += ['S003'] + ['S002'] + ['S020']
    for column in df_in.columns:
        vals = df_in[column].unique()
        if 1 in vals and 0 in vals:
            pass
        elif column in total_reversed_columns:
            pass
        else:
            df_in[column] = df_in[column].replace(dic)
    return df_in

## filter by wave number
def group_by_wave(wave,df_in):
    df_out = df_in[df_in['S002'] == wave]
    return df_out


## change negative numbers to missing values
def change_to_nan(df_in):
    df_out = df_in.copy()
    for column in df_out:
        df_out[column] = df_out[column].apply(lambda x: x if x>=0 else np.nan)
    return df_out

## only keep columns that have over 50% answer rate
def keep_answered(df_in):
    dic = (df_in.count()/df_in.shape[0]).to_dict()
    l = [key for key,value in dic.iteritems() if value > .7]
    return l


def output_cleaned_df(df):
    best = sorted(keep_answered(df))
    for_transform = best[:-3]
    df_final = df[for_transform]
    return df_final

def output_cleaned_df_withcountry(df):
    best = sorted(keep_answered(df))
    for_transform = best
    df_final = df[for_transform]
    return df_final

# def remove_negatives(df_in):
#     for column in df_in.columns:
#         column_mean = df_in[df_in[column] > 0][column].mean()
#         df_in[column] = df_in[column].apply(lambda x: x if x >= 0 else column_mean)
#     return df_in

def get_dummies(df_in):
    df_out = df_in.copy()
    dummy_cols = ['A025','A026','A044','A045','A050','A169','A174']
    for col in dummy_cols:
        if col in df_out.columns:
            dummies = pd.get_dummies(df_out[col],drop_first = True)
            d =  {dum_col: col +str(dum_col) for dum_col in dummies.columns}
            dummies = dummies.rename(index = int,columns =  d)
            print dummies
            print df_out.index
            #print dummies
            #print dummies.shape
            df_out = pd.concat((df_out,dummies),axis = 1)
            df_out.drop(col,axis = 1,inplace =True)
            print df_out
    return df_out

def most_important_cols(v_matrix,df):
    #features = [i for i,l in enumerate(v_matrix[0,:]) if abs(l) > .2]
    features = np.argsort(np.abs(v_matrix[0,:]))[::-1]
    cols = df.columns
    important_cols = cols[features]
    return important_cols
