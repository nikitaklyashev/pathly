import sqlite3

db = sqlite3.connect('pathly.db')

cursor = db.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        username VARCHAR(255) NOT NULL,
        password_hash VARCHAR(255) NOT NULL         
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS roadmaps (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        title VARCHAR(255) NOT NULL,
        description TEXT NOT NULL        
    )
""")

cursor.execute("""
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

cursor.execute("""
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




db.commit()

db.close()