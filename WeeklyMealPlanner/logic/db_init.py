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
    CREATE TABLE November_2020 (
        date INTEGER PRIMARY KEY,
        day VARCHAR,
        breakfast_primary VARCHAR,
        breakfast_secondary VARCHAR,
        breakfast_price FLOAT,
        supper_primary VARCHAR,
        supper_secondary VARCHAR,
        supper_price FLOAT,
        day_price FLOAT
    )
    '''
)

connection.commit()
connection.close()