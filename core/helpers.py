import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# Load env vars
load_dotenv()
print(os.getenv("DATABASE_URL"))

# Explicit DB URL
url = "postgresql://postgres.ykpannaonwuhpivkwohz:%2A_%2BAygd6r6Pkh%24%24@aws-1-us-east-2.pooler.supabase.com:5432/postgres"

# Create engine
engine = create_engine(url, pool_pre_ping=True)

# Test connection
with engine.connect() as conn:
    result = conn.execute(text("select current_database(), inet_server_addr(), inet_server_port();"))
    print(result.fetchall())
