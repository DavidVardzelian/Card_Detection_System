from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('config/streams.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    streams = conn.execute('SELECT * FROM streams').fetchall()
    conn.close()
    return render_template('index.html', streams=streams)

@app.route('/add', methods=['POST'])
def add_stream():
    url = request.form['url']
    card_proxy_ip = request.form['card_proxy_ip']
    conn = get_db_connection()
    conn.execute('INSERT INTO streams (url, card_proxy_ip) VALUES (?, ?)', (url, card_proxy_ip))
    conn.commit()
    conn.close()
    return jsonify({'status': 'success'})

@app.route('/update/<int:id>', methods=['POST'])
def update_stream(id):
    url = request.form['url']
    card_proxy_ip = request.form['card_proxy_ip']
    conn = get_db_connection()
    conn.execute('UPDATE streams SET url = ?, card_proxy_ip = ? WHERE id = ?', (url, card_proxy_ip, id))
    conn.commit()
    conn.close()
    return jsonify({'status': 'success'})

@app.route('/delete/<int:id>', methods=['POST'])
def delete_stream(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM streams WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005)
