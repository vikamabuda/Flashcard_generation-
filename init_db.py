import sqlite3

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

if __name__ == '__main__':
    init_db()
