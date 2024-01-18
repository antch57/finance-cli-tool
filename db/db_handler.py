from mysql.connector import Error, pooling

class DBHandler:
    def __init__(self, host, port, user, password, database):
        try:
            self.connection_pool = pooling.MySQLConnectionPool(
                pool_size=5,
                host=host,
                port=port,
                user=user,
                password=password,
                database=database
            )

        except Error as e:
            print(f'Error connecting to database: {e}')

    def get_connection(self):
        return self.connection_pool.get_connection()
