import csv
import sqlite3
from datetime import datetime

DATABASE = 'flashcards.db'

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

# Example usage
load_flashcards_from_csv('flashcards.csv')
