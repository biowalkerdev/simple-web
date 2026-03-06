from flask import Flask, request, render_template_string, make_response, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'super_secret_key_123'

users_db = {
    'admin': 'admin123',
    'user': 'password'
}

@app.route('/')
def index():
    with open('index.html', 'r') as f:
        return render_template_string(f.read())

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    if username in users_db and users_db[username] == password:
        return "Welcome " + username
    return "Login failed"

@app.route('/search')
def search():
    query = request.args.get('q', '')
    return f"Search results for: {query}"

@app.route('/profile')
def profile():
    user = request.args.get('user')
    return f"<h1>Profile: {user}</h1>"

@app.route('/setcookie')
def setcookie():
    resp = make_response("Cookie set")
    resp.set_cookie('session', request.args.get('value', ''))
    return resp

@app.route('/getcookie')
def getcookie():
    return request.cookies.get('session', 'No cookie')

@app.route('/admin')
def admin():
    if request.cookies.get('role') == 'admin':
        return "Admin panel"
    return "Access denied"

@app.route('/reflect')
def reflect():
    data = request.args.get('data', '')
    return data

@app.route('/error')
def error():
    msg = request.args.get('msg', '')
    return f"<script>alert('Error: {msg}')</script>"

@app.route('/redirect')
def redirect():
    url = request.args.get('url', '/')
    return f'<meta http-equiv="refresh" content="0;url={url}">'

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    return '''
    <form method="POST" enctype="multipart/form-data">
        <input type="file" name="file">
        <input type="submit">
    </form>
    '''

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)