from app.database.models import init_db
from app.database.connection import init_db_pool

if __name__ == "__main__":
    init_db_pool()
    init_db()
    print("Database initialized successfully")