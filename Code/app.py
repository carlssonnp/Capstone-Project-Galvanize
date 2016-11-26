from flask import Flask, request
app = Flask(__name__)
from analyze_surveys import Wave
import pickle


import pandas as pd


# home page
# @app.route('/')
# def index():
#     return '<a href="https://plot.ly/~nordik91/20.embed">look at the graph</a>'
@app.route('/')
def index():
    return 'hi'

@app.route('/coolgraph')
def show_graph():
    with open('html_for_graph.html') as f:
        line = f.read()
    return line


@app.route('/all')
def wave_all():
    with open('WaveAll.html') as f:
        line = f.read()
    return line

@app.route('/6')
def wave_6():
    with open('Wave6.html') as f:
        line = f.read()
    return line

@app.route('/5')
def wave_5():
    with open('Wave5.html') as f:
        line = f.read()
    return line

@app.route('/4')
def wave_4():
    with open('Wave4.html') as f:
        line = f.read()
    return line

@app.route('/3')
def wave_3():
    with open('Wave3.html') as f:
        line = f.read()
    return line

@app.route('/2')
def wave_2():
    with open('Wave2.html') as f:
        line = f.read()
    return line

@app.route('/1')
def wave_1():
    with open('Wave1.html') as f:
        line = f.read()
    line = line + '''
        <form action="/showmap" method='POST' >
            <input type="text" name="user_input" />
            <input type="submit" />
        </form>'''
    return line

@app.route('/submit')
def submission_page():
    return '''<p> Enter wave number (1-6) below: </p>
        <form action="/showmap" method='POST' >
            <input type="text" name="user_input" />
            <input type="submit" />
        </form>
        '''

@app.route('/showmap', methods=['POST'] )
def word_counter():
    line = '''<head>
		<meta charset="UTF-8">
		<title>Nils-Carlsson</title>
		<link rel="stylesheet" href="static/personal2.css">
	</head>'''
    wave = request.form['user_input'].split()[0]
    pc = int(request.form['user_input'].split()[1])
    ht = 'html_files/Wave' +' ' + str(wave) +'_PC' + str(pc) + '.html'

    with open(ht) as f:
        line+= f.read()

    line+= '''<p> Questions most correlated with this component: <br/> <br/> '''
    df = pd.read_csv('codebook.csv', header = -1)
    df.index = df[2]

    correlation_dic = pickle.load(open('pickled_correlation_dictionaries/Wave' + str(wave) + '_correlation_dic.pkl','r'))
    for i in xrange(3):
        line+= ''' Question %s: %s (Correlation: %s) <br/>''' %(correlation_dic[pc].index[i],df.loc[correlation_dic[pc].index[i],3],round(correlation_dic[pc][i],2))
    #line+= '''<p> Questions most correlated with this component: <br/> %s, %s </p>''' %(wave1.survey.iloc[1,1],t)
    line += '</p>'
    line+= 'Enter wave number (1-6) below: '
    line+= '''
        <form action="/showmap" method='POST' >
            <input type="text" name="user_input" />
            <input type="submit" />
        </form>
        '''

    return line


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081, debug=True)
