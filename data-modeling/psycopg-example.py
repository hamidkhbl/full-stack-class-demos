# using psycopg2
import psycopg2

connection = psycopg2.connect('dbname=postgres user=postgres')

cursor = connection.cursor()

cursor.execute(
    '''
    CREATE TABLE table3 (
        id INTEGER PRIMARY KEY,
        Completed BOOLEAN
    );
    '''
)

cursor.execute(
    '''
    INSERT INTO table3 VALUES(1,False)
    '''
)

connection.commit()
cursor.close()
connection.close()