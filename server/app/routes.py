from app import app
import sqlite3

conn = sqlite3.connect('/home/pi/data.db')

@app.route('/')
@app.route('/index')
def index():
    print('test')
    return 'test'

@app.route('/samples')
def samples():
    for row in conn.execute('select * from samples'):
        print(row)
    return 'test'

@app.route('/dft')
def dft():
    for row in conn.execute('select * from dft'):
        print(row)
    return 'test'