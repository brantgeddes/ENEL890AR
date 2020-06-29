from app import app
import sqlite3
from flask import jsonify

conn = sqlite3.connect('/home/pi/enel/data.db')

@app.route('/samples')
def samples():
    values = []
    for row in conn.execute('select value from samples'):
        values.append(row[0])
    return jsonify({ "values": values })

@app.route('/dft')
def dft():
    real = []
    imag = []
    for row in conn.execute('select real, imag from dft'):
        real.append(row[0])
        imag.append(row[1])
    return jsonify({ "real": real, "imag": imag })
