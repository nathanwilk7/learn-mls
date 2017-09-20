rm m.db
sqlite3 m.db < create_db_schema.sql
python insert_match.py
