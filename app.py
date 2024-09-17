import csv
import sqlite3
from datetime import datetime
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)
DATABASE = 'flashcards.db'

def init_db():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS flashcards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            mistake_type TEXT,
            original_sentence TEXT,
            corrected_sentence TEXT,
            review_count INTEGER,
            next_review DATETIME
        )
    ''')
    conn.commit()
    conn.close()

def load_flashcards_from_csv(file_path):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            student_id = row['Student_ID']
            mistake_type = row['Mistake_Type']
            original = row['Original_Sentence']
            corrected = row['Corrected_Sentence']
            c.execute('''
                INSERT INTO flashcards (student_id, mistake_type, original_sentence, corrected_sentence, review_count, next_review)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (student_id, mistake_type, original, corrected, 0, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    
    conn.commit()
    conn.close()

def get_students():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('SELECT DISTINCT student_id FROM flashcards')
    students = c.fetchall()
    conn.close()
    return [student[0] for student in students]

@app.route('/')
def index():
    students = get_students()
    print("Students:", students)  # Debugging line
    return render_template('index.html', students=students)

@app.route('/flashcard')
def flashcard():
    student_id = request.args.get('student_id')
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('''
        SELECT id, mistake_type, original_sentence, corrected_sentence, review_count
        FROM flashcards
        WHERE student_id = ?
        AND next_review <= ?
        ORDER BY RANDOM()
        LIMIT 1
    ''', (student_id, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    flashcard = c.fetchone()
    conn.close()
    
    if flashcard:
        return jsonify({
            'id': flashcard[0],
            'mistake_type': flashcard[1],
            'original_sentence': flashcard[2],
            'corrected_sentence': flashcard[3],
            'review_count': flashcard[4]
        })
    return jsonify({'message': 'No flashcards available'})

@app.route('/review/<int:flashcard_id>', methods=['POST'])
def review(flashcard_id):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    
    c.execute('SELECT review_count FROM flashcards WHERE id = ?', (flashcard_id,))
    review_count = c.fetchone()[0]
    
    # Simple spaced repetition logic (increment review count and adjust review interval)
    review_count += 1
    next_review = datetime.now()
    if review_count == 1:
        next_review = next_review.replace(day=next_review.day + 1)  # Review in 1 day
    elif review_count == 2:
        next_review = next_review.replace(day=next_review.day + 3)  # Review in 3 days
    elif review_count == 3:
        next_review = next_review.replace(day=next_review.day + 7)  # Review in 7 days
    else:
        next_review = next_review.replace(day=next_review.day + 14)  # Review in 14 days
    
    c.execute('UPDATE flashcards SET review_count = ?, next_review = ? WHERE id = ?', (review_count, next_review.strftime('%Y-%m-%d %H:%M:%S'), flashcard_id))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Flashcard reviewed'})

@app.route('/debug/students')
def debug_students():
    students = get_students()
    return jsonify(students)

if __name__ == '__main__':
    init_db()
    load_flashcards_from_csv('flashcards.csv')  # Load flashcards when starting the app
    app.run(debug=True)
