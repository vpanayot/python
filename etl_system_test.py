import sqlite3
from etl_system import ETL, SourceFactory, SinkFactory

# Read from simulation source and print to console
ETL().source('Simulation Source', 'sim').sink('Console Target', 'console').run()

# Create Source and Target objects
file_src1 = SourceFactory.create_source('Json Source 1', 'file', 'messages.json')
file_src2 = SourceFactory.create_source('Json Source 2', 'file', 'messages.json')
db_tgt = SinkFactory.create_sink('DB Sink', 'sqlite', 'test.db', 'msg_table')
console_tgt = SinkFactory.create_sink('Console Target', 'console')

# Read from json source file and print to console
etl1 = ETL(file_src1, console_tgt)
etl1.run()

# Cleanup table
db_tgt.cleanup_table()

# Read from json source file and write to SQLite database
etl2 = ETL(file_src2, db_tgt)
etl2.run()

# Check data in table
print('Checking data in SQLite table')
conn = sqlite3.connect('test.db')
cursor = conn.cursor()

cursor.execute("SELECT * FROM msg_table")
rows = cursor.fetchall()
for row in rows:
    print(row)

conn.close()

