from flask import Flask, request
import pickle
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    '''
    Creates index page
    '''
    return 'This is my webpage'


@app.route('/submit')
def submission_page():
    '''
    Creates page for user to submit query
    '''
    return '''<p> Enter wave number (1-6) below: </p>
            <form action="/showmap" method='POST' >
            <input type="text" name="user_input" />
            <input type="submit" />
            </form>
           '''

@app.route('/showmap', methods=['POST'] )
def word_counter():
    '''
    Shows results of user query on world map.
    '''
    line = '''
        <head>
		<meta charset="UTF-8">
		<title>Nils-Carlsson</title>
		<link rel="stylesheet" href="static/personal3.css">
	    </head>
        '''
    # first input is wave number (time period)
    wave = request.form['user_input'].split()[0]
    #second input is principal component number
    pc = int(request.form['user_input'].split()[1])
    #use appropriate html file based on wave and pc
    html_file = 'html_files/Wave' +' ' + str(wave) +'_PC' + str(pc) + '.html'
    with open(html_file) as f:
        line+= f.read()

    # display questions most correlated with principal component, along with question description and numerical correlation
    line+= '''<p> Questions most correlated with this component: <br/> <br/> '''
    codebook = pd.read_csv('codebook.csv', header = -1)
    # make the index of the codebook df the names of the questions
    codebook.index = codebook[2]
    correlation_dic = pickle.load(open('pickled_correlation_dictionaries/Wave' + str(wave) + '_correlation_dic.pkl','r'))
    for i in xrange(3):
        line+= ''' Question %s: %s (Correlation: %s) <br/>''' %(correlation_dic[pc].index[i],
        codebook.loc[correlation_dic[pc].index[i],3],round(correlation_dic[pc][i],2))

    # allow user to enter another query
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
    app.run(host='0.0.0.0', port=8080, debug=True)
