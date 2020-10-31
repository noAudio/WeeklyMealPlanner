from sqlite3 import connect
from sqlite3.dbapi2 import Connection, Cursor

connection: Connection = connect('foods.db')
cmd: Cursor = connection.cursor()

cmd.execute(
    '''
    CREATE TABLE Foods (
        id VARCHAR PRIMARY KEY,
        name VARCHAR,
        food_type VARCHAR,
        food_class VARCHAR,
        price FLOAT
    )
    '''
)
cmd.execute(
    '''
    CREATE TABLE Week (
        id VARCHAR PRIMARY KEY,
        sunday VARCHAR,
        monday VARCHAR,
        tuesday VARCHAR,
        wednesday VARCHAR,
        thursday VARCHAR,
        friday VARCHAR,
        saturday VARCHAR,
        total_cost FLOAT
    )
    '''
)

connection.commit()
connection.close()