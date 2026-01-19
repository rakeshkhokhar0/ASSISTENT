import sqlite3

DB_NAME = "assistient.db"
class DatabseConnection:
    def __init__(self) -> None:
        self.conn = None

    def __enter__(self) -> sqlite3.Cursor:
        self.conn = sqlite3.connect(DB_NAME)
        return self.conn.cursor()
    
    def __exit__(self,exc_type, exc_value, traceback) ->None:
        if exc_type or exc_value or traceback:
            self.conn.close() # type: ignore
        else:
            self.conn.commit() # type: ignore
            self.conn.close()  # type: ignore