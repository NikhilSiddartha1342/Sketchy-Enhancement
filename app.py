import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session, send_file
from werkzeug.utils import secure_filename
import uuid
import cv2
from filters.sketch import apply_sketch
from filters.cartoonize import apply_cartoonize
from filters.vintage import apply_vintage
from filters.hdr import apply_hdr
from filters.style_transfer import apply_style_transfer

app = Flask(__name__)
app.secret_key = 'secret'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['OUTPUT_FOLDER'] = 'static/outputs'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

if not os.path.exists(app.config['OUTPUT_FOLDER']):
    os.makedirs(app.config['OUTPUT_FOLDER'])

def get_db_connection():
    db_path = os.path.join(os.path.dirname(__file__), 'users.db')
    return sqlite3.connect(db_path)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT)")
        c.execute("SELECT * FROM users WHERE username = ?", (username,))
        if c.fetchone():
            conn.close()
            return 'User already exists!'
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        conn.close()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        if c.fetchone():
            session['username'] = username
            conn.close()
            return redirect(url_for('dashboard'))
        else:
            conn.close()
            return 'Invalid credentials!'
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        file = request.files['image']
        filter_type = request.form['filter']
        if file:
            filename = secure_filename(file.filename)
            unique_name = str(uuid.uuid4()) + os.path.splitext(filename)[1]
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_name)
            file.save(filepath)

            output_filename = 'filtered_' + unique_name
            output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)

            img = cv2.imread(filepath)

            if filter_type == 'sketch':
                result = apply_sketch(img)
            elif filter_type == 'cartoon':
                result = apply_cartoonize(img)
            elif filter_type == 'vintage':
                result = apply_vintage(img)
            elif filter_type == 'hdr':
                result = apply_hdr(img)
            elif filter_type == 'style':
                result = apply_style_transfer(img)
            else:
                result = img

            cv2.imwrite(output_path, result)
            save_history(session['username'], unique_name, output_filename)
            return render_template('result.html', filename=output_filename)

    return render_template('upload.html')

@app.route('/history')
def view_history():
    if 'username' not in session:
        return redirect(url_for('login'))
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS history (username TEXT, original TEXT, result TEXT)")
    c.execute("SELECT original, result FROM history WHERE username = ?", (session['username'],))
    data = c.fetchall()
    conn.close()
    return render_template('history.html', history=data)

def save_history(username, original_img, result_img):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS history (username TEXT, original TEXT, result TEXT)")
    c.execute("INSERT INTO history (username, original, result) VALUES (?, ?, ?)", (username, original_img, result_img))
    conn.commit()
    conn.close()

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

@app.route('/download/<filename>')
def download(filename):
    path = os.path.join(app.config['OUTPUT_FOLDER'], filename)
    return send_file(path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
