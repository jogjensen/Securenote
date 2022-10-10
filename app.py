from flask import Flask, render_template, request, url_for, flash, redirect, abort
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = '5362ee004e43a663885d45fbc8c57667a499af87603dc9a6'


def get_db_connection():
    conn = sqlite3.connect('C:\\Users\\Jannich\\PycharmProjects\\flaskProject\\notedb')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/')
def home():
    conn = get_db_connection()
    notes = conn.execute('SELECT * FROM notes').fetchall()
    conn.close()
    return render_template('home.html', notes=notes)


@app.route('/', methods=['POST'])
def user_form():
    if request.method == 'POST':
        title = request.form['title']
        note = request.form['cryptTextArea']

        if not title:
            flash('Der skal benyttes en titel!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO notes (title, note) VALUES (?, ?)', (title, note))
            conn.commit()
            conn.close()
    return render_template('home.html')


def get_note(note_id):
    conn = get_db_connection()
    note = conn.execute('SELECT * FROM notes WHERE id = :noteid', {"noteid": note_id}).fetchone()
    conn.commit()
    conn.close()
    if note is None:
        abort(404)
    return note


@app.route('/note/<int:note_id>')
def show_note(note_id):
    note = get_note(note_id)
    return render_template('note.html', note=note)


@app.route('/edit/<int:note_id>', methods=('GET', 'POST'))
def edit_note(note_id):
    note = get_note(note_id)
    if request.method == 'POST':
        edited_title = request.form['edited_title']
        edited_note = request.form['edited_note']

        if not edited_title:
            flash('Title is required!')

        elif not edited_note:
            flash('Note is required!')

        else:
            conn = get_db_connection()
            conn.execute('UPDATE notes SET title = ?, note = ? WHERE id = ?', (edited_title, edited_note, note_id))
            conn.commit()
            conn.close()
            return redirect(url_for('edit_note', note_id=note_id))
    return render_template('edit.html', note=note)


if __name__ == '__main__':
    app.run()
