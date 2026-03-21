from sqlalchemy import create_engine
from urllib.parse import quote_plus

DB_USER = "root"
DB_PASSWORD = quote_plus("SHIvam2005@$")
DB_HOST = "127.0.0.1"
DB_PORT = "3306"
DB_NAME = "insurance_db"

engine = create_engine(
    f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

print("✅ DB Connected")