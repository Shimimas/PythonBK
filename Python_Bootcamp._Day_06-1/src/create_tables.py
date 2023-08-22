import psycopg2

conn = psycopg2.connect(dbname="selectel", user="selectel", password="selectel", host="127.0.0.1", port="5432")
cursor = conn.cursor()
try:
    cursor.execute("CREATE TABLE ships (id SERIAL PRIMARY KEY, alignment VARCHAR(50), name VARCHAR(50), classes VARCHAR(50), length FLOAT, crewSize INTEGER, armed BOOL, officers VARCHAR(2000))")
except psycopg2.ProgrammingError:
    pass
conn.commit()
try:
    cursor.execute("CREATE TABLE traitors (id SERIAL PRIMARY KEY, first_name VARCHAR(50), last_name VARCHAR(50), rank VARCHAR(50))")
except psycopg2.ProgrammingError:
    pass
conn.commit()
cursor.close()
conn.close()