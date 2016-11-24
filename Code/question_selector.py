# the following functions, create_columns_a - create_columns_i, determine what questions to use from each section
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
    bad_cols.append(['A0' + str(col_num) for col_num in xrange(10,20)])
    bad_cols.append(['A0' + str(col_num) for col_num in xrange(25,57)])
    bad_cols.append(['A0' + str(col_num) for col_num in xrange(64,100)])
    bad_cols.append(['A' + str(col_num) for col_num in xrange(100,107)])
    bad_cols.append(['A' + str(col_num) for col_num in xrange(123,166)])
    bad_cols.append(['A' + str(col_num) for col_num in xrange(168,170)])
    bad_cols.append(['A' + str(col_num) for col_num in xrange(174,200)])
    bad_cols.append(['A' + str(col_num) for col_num in xrange(208,213)])

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
    bad_cols.append(['B00' + str(col_num) for col_num in xrange(8,10)])
    bad_cols.append(['B0' + str(col_num) for col_num in xrange(10,18)])

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
    for col_num in xrange(1,6):
        bad_cols.append('C00' + str(col_num))
    bad_cols.append('C009')
    for col_num in xrange(10,31):
        bad_cols.append('C0' + str(col_num))
    for col_num in xrange(42,62):
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
    for col_num in xrange(3,10):
        bad_cols.append('D00' + str(col_num))
    for col_num in xrange(10,20):
        bad_cols.append('D0' + str(col_num))
    for col_num in xrange(21,26):
        bad_cols.append('D0' + str(col_num))
    for col_num in xrange(44,54):
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
    for col_num in xrange(1,7):
        bad_cols.append('E00' + str(col_num))
    for col_num in xrange(11,13):
        bad_cols.append('E0' + str(col_num))
    for col_num in xrange(14,21):
        bad_cols.append('E0' + str(col_num))
    bad_cols.append('E022')
    for col_num in xrange(25,33):
        bad_cols.append('E0' + str(col_num))
    for col_num in xrange(48,57):
        bad_cols.append('E0' + str(col_num))
    bad_cols.append('E062')
    for col_num in xrange(69,100):
        bad_cols.append('E0' + str(col_num))
    for col_num in xrange(100,104):
        bad_cols.append('E' + str(col_num))
    for col_num in xrange(118,120):
        bad_cols.append('E' + str(col_num))
    for col_num in xrange(126,130):
        bad_cols.append('E' + str(col_num))
    for col_num in xrange(131,133):
        bad_cols.append('E' + str(col_num))
    for col_num in xrange(135,140):
        bad_cols.append('E' + str(col_num))
    for col_num in xrange(144,146):
        bad_cols.append('E' + str(col_num))
    for col_num in xrange(178,184):
        bad_cols.append('E' + str(col_num))
        bad_cols.append('E187')
    for col_num in xrange(190,196):
        bad_cols.append('E' + str(col_num))
    for col_num in xrange(190,196):
        bad_cols.append('E' + str(col_num))
    bad_cols.append('E197')
    for col_num in xrange(199,203):
        bad_cols.append('E' + str(col_num))
    for col_num in xrange(199,203):
        bad_cols.append('E' + str(col_num))
    bad_cols.append('E204')
    bad_cols.append('E206')
    for col_num in xrange(209,212):
        bad_cols.append('E' + str(col_num))
    for col_num in xrange(213,220):
        bad_cols.append('E' + str(col_num))
    for col_num in xrange(221,224):
        bad_cols.append('E' + str(col_num))
    for col_num in xrange(237,242):
        bad_cols.append('E' + str(col_num))
    for col_num in xrange(248,255):
        bad_cols.append('E' + str(col_num))
    for col_num in xrange(256,263):
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
    for col_num in xrange(4,10):
        bad_cols.append('F00' + str(col_num))
    for col_num in xrange(10,12):
        bad_cols.append('F0' + str(col_num))
    for col_num in xrange(13,28):
        bad_cols.append('F0' + str(col_num))
    bad_cols.append('F029')
    for col_num in xrange(31,34):
        bad_cols.append('F0' + str(col_num))
    bad_cols.append('F062')
    for col_num in xrange(35,61):
        bad_cols.append('F0' + str(col_num))
    for col_num in xrange(64,66):
        bad_cols.append('F0' + str(col_num))
    for col_num in xrange(88,93):
        bad_cols.append('F0' + str(col_num))
    bad_cols.append('F098')
    bad_cols.append('F162')
    for col_num in xrange(176,186):
        bad_cols.append('F' + str(col_num))
    for col_num in xrange(188,190):
        bad_cols.append('F' + str(col_num))
    bad_cols.append('F192')
    for col_num in xrange(200,202):
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
    for col_num in xrange(4,6):
        bad_cols.append('G00' + str(col_num))
    for col_num in xrange(7,10):
        bad_cols.append('G00' + str(col_num))
    for col_num in xrange(10,14):
        bad_cols.append('G0' + str(col_num))
    for col_num in xrange(15,19):
        bad_cols.append('G0' + str(col_num))
    bad_cols.append('G022')
    for col_num in xrange(24,28):
        bad_cols.append('G0' + str(col_num))
    good_cols = set(columns) - set(bad_cols)
    return sorted(list(good_cols))


def create_columns_h():
    return ['H001']


def create_columns_i():
    return ['I001', 'I002']
