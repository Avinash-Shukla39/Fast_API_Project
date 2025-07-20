from app.database.connection import get_db_connection

def init_db():
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS videos (
                id UUID PRIMARY KEY,
                filename VARCHAR(255) NOT NULL,
                encrypted_data BYTEA NOT NULL,
                uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                content_type VARCHAR(100)
            );
        """)
        
        conn.commit()
    except Exception as e:
        print(f"Error initializing database: {e}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            cursor.close()
            conn.close()

def create_video_record(video_id, filename, encrypted_data, content_type):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO videos (id, filename, encrypted_data, content_type) VALUES (%s, %s, %s, %s)",
            (video_id, filename, encrypted_data, content_type)
        )
        
        conn.commit()
    except Exception as e:
        print(f"Error creating video record: {e}")
        if conn:
            conn.rollback()
        raise
    finally:
        if conn:
            cursor.close()
            conn.close()

def get_video_by_id(video_id):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT encrypted_data, content_type FROM videos WHERE id = %s",
            (video_id,)
        )
        
        return cursor.fetchone()
    except Exception as e:
        print(f"Error fetching video: {e}")
        raise
    finally:
        if conn:
            cursor.close()
            conn.close()