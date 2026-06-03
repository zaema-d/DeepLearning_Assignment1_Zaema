from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os
import base64

app = Flask(__name__)
#DATABASE = 'database.db'
DATABASE = os.path.join(os.path.dirname(__file__), 'database.db')

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

# def get_db():
#     db = getattr(app, '_database', None)
#     if db is None:
#         db = app._database = sqlite3.connect(DATABASE, check_same_thread=False)
#     return db
from flask import g

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE, check_same_thread=False)
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(app, '_database', None)
    if db is not None:
        db.close()

def get_decoded_image(photo_data):
    try:
        return base64.b64decode(photo_data.split(',')[1])
    except IndexError:
        print(f"Error: Invalid photo data received - {photo_data[:100]}...")  # Print the first 100 chars for debugging
        return None        

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        photo1_data = request.form.get('photo1Data')
        photo2_data = request.form.get('photo2Data')

        photo1_binary = get_decoded_image(photo1_data)
        photo2_binary = get_decoded_image(photo2_data)

        if not photo1_binary or not photo2_binary:
            # Handle the error - return an error message to the user
            return "Invalid photo data received. Please capture both photos and try again.", 400

        db = get_db()
        cur = db.cursor()
        cur.execute("INSERT INTO users (name, email, photo1, photo2) VALUES (?, ?, ?, ?)", (name, email, photo1_binary, photo2_binary))
        db.commit()

        return redirect(url_for('index'))

    return render_template('register.html')

@app.route('/')
def index():
    return "Hello World!"

if __name__ == "__main__":
    if not os.path.exists(DATABASE):
        init_db()
    app.run(debug=True)
