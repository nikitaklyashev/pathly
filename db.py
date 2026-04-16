import sqlite3
from UserLogin import UserLogin

DB_PATH = "pathly.db"

def init_db():
    db = get_db()

    db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            username VARCHAR(255) NOT NULL,
            password_hash VARCHAR(255) NOT NULL         
        )
    """)

    db.execute("""
        CREATE TABLE IF NOT EXISTS roadmaps (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            title VARCHAR(255) NOT NULL,
            description TEXT NOT NULL        
        )
    """)

    db.execute("""
        CREATE TABLE IF NOT EXISTS steps (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            roadmap_id INTEGER NOT NULL, 
            title VARCHAR(255) NOT NULL,
            description TEXT NOT NULL,
            order_index INTEGER NOT NULL,
            
            FOREIGN KEY (roadmap_id) REFERENCES roadmaps(id) ON DELETE CASCADE,

            UNIQUE (roadmap_id, order_index)       
        )
    """)

    db.execute("""
        CREATE TABLE IF NOT EXISTS user_step_progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            user_id INTEGER NOT NULL,
            step_id INTEGER NOT NULL,
            status TEXT NOT NULL DEFAULT 'not_started',
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,  

            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (step_id) REFERENCES steps(id) ON DELETE CASCADE,

            UNIQUE (user_id, step_id)      
        )
    """)

    db.execute("""
        CREATE TABLE IF NOT EXISTS favorites (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            roadmap_id INTEGER NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (roadmap_id) REFERENCES roadmaps(id) ON DELETE CASCADE,
            UNIQUE(user_id, roadmap_id)
        )
    """)

    db.commit()
    db.close()

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def get_user_by_id(user_id):
    db = get_db()

    try:
        cursor = db.execute("SELECT * FROM users WHERE id = ? LIMIT 1", (user_id,))
        res = cursor.fetchone()
        if not res:
            return False
        
        return res
    except sqlite3.Error as e:
        print("Ошибка: " + str(e))
        return None
    finally:
        db.close()

def get_user_by_login(username):
    db = get_db()

    try:
        cursor = db.execute("SELECT * FROM users WHERE username = ? LIMIT 1", (username,))
        res = cursor.fetchone()
        if not res:
            return False
        return res
    except sqlite3.Error as e:
        print("Ошибка: " + str(e))
        return False
    finally:
        db.close()

def get_roadmaps():
    db = get_db()

    try:
        cursor = db.execute("SELECT * FROM roadmaps")
        res = cursor.fetchall()
        if not res:
            return False
        return res
    except sqlite3.Error as e:
        print("Ошибка получения данных из БД" + str(e))
        return False
    finally:
        db.close()

def get_favs(user_id):
    db = get_db()

    try:
        cursor = db.execute("SELECT * FROM favorites WHERE user_id = ?", (user_id,))
        res = cursor.fetchall()
        if not res:
            return []
        return res
    except sqlite3.Error as e:
        print("Ошибка: " + str(e))
        return False  
    finally:
        db.close()

def get_fav(user_id, roadmap_id):
    db = get_db()

    try:
        cursor = db.execute("SELECT * FROM favorites WHERE user_id = ? AND roadmap_id = ?", 
            (user_id, roadmap_id))
        res = cursor.fetchall()
        if not res:
            return False
        return res
    except sqlite3.Error as e:
        print("Ошибка: " + str(e))
    finally:
        db.close()
    return False

def add_fav(user_id, roadmap_id):
    db = get_db()

    try:
        cursor = db.execute("INSERT INTO favorites (user_id, roadmap_id) VALUES(?, ?)", 
            (user_id, roadmap_id))

        db.commit()        
        return True
    except sqlite3.Error as e:
        print("Ошибка: " + str(e))
    finally:
        db.close()
    return False

def remove_fav(user_id, roadmap_id):
    db = get_db()

    try:
        cursor = db.execute("DELETE FROM favorites WHERE user_id = ? AND roadmap_id = ?", 
            (user_id, roadmap_id))

        db.commit()        
        return True
    except sqlite3.Error as e:
        print("Ошибка: " + str(e))
        return False   
    finally:
        db.close()
