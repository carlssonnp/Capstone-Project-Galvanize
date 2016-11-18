from flask import Flask, request
app = Flask(__name__)



# home page
# @app.route('/')
# def index():
#     return '<a href="https://plot.ly/~nordik91/20.embed">look at the graph</a>'
@app.route('/')
def index():
    return 'hi'

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
    return '''
        <form action="/showmap" method='POST' >
            <input type="text" name="user_input" />
            <input type="submit" />
        </form>
        '''

@app.route('/showmap', methods=['POST'] )
def word_counter():
    wave = request.form['user_input']
    ht = 'Wave' + str(wave) + '.html'
    with open(ht) as f:
        line = f.read()
    line+= '''
        <form action="/showmap" method='POST' >
            <input type="text" name="user_input" />
            <input type="submit" />
        </form>
        '''
    return line


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081, debug=True)
