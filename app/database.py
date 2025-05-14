import sqlite3
from bs4 import BeautifulSoup

DB_PATH = "data.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS people (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            last_name TEXT,
            first_name TEXT,
            middle_name TEXT,
            birthdate TEXT,
            phone TEXT,
            position TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_table_from_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find("table")
    rows = table.find_all("tr")[1:]  # Пропускаем заголовок

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    count = 0
    for row in rows:
        cols = row.find_all("td")
        if len(cols) != 6:
            continue
        c.execute("""
            INSERT INTO people (last_name, first_name, middle_name, birthdate, phone, position)
            VALUES (?, ?, ?, ?, ?, ?)
        """, [col.get_text(strip=True) for col in cols])
        count += 1
    conn.commit()
    conn.close()
    return count

def search_people(query):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    pattern = f"%{query}%"
    c.execute("""
        SELECT last_name, first_name, middle_name, birthdate, phone, position
        FROM people
        WHERE last_name LIKE ? OR first_name LIKE ? OR phone LIKE ? OR position LIKE ?
    """, (pattern, pattern, pattern, pattern))
    results = c.fetchall()
    conn.close()
    return results
