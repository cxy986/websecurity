import os
from pathlib import Path
import sqlite3

database_path = Path(os.environ.get("DATABASE_PATH", Path(__file__).resolve().parent / "users.db"))
database_path.parent.mkdir(parents=True, exist_ok=True)
conn = sqlite3.connect(database_path)

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    role TEXT NOT NULL
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    content TEXT NOT NULL
)
""")

for username, password, role in [
    ("admin", "123456", "admin"),
    ("test", "test123", "user"),
]:
    cursor.execute("SELECT 1 FROM users WHERE username = ?", (username,))
    if cursor.fetchone() is None:
        cursor.execute(
            "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
            (username, password, role),
        )

conn.commit()
conn.close()

print("数据库创建成功！")
