from sqlite3.dbapi2 import Connection, Cursor, connect


class DBConnection:
    '''
    Establishes connection to database.
    Also allows database commit and disconnection via _commit_disconnect_db().
    '''
    connection: Connection
    _db: str = 'foods.db'

    def __init__(self) -> None:
        '''
        Access the db to read, add, update, delete and/or remove tables and table entries
        '''
        self._connect_db()

    def _connect_db(self) -> None:
        '''
        Instantiate a connection to the database.
        '''
        self.connection: Connection = connect(self._db)
        self.cmd: Cursor = self.connection.cursor()
    
    def _commit_disconnect_db(self) -> None:
        '''
        Commit changes and close database connection.
        '''
        self.connection.commit()
        self.connection.close()
