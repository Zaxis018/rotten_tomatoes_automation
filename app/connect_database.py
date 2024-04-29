"""
This module provides funcitonality to connect to database
"""

import sqlite3

class DatabaseOperation:
    """Connects to a database"""

    def __init__(self) -> None:
        '''initialize a database'''
        self.conn = None
        self.cursor = None
        try:
            self.conn = sqlite3.connect('tomatoes.db')
            self.cursor =  self.conn.cursor()
            print(sqlite3.version)
        except sqlite3.Error as e:
            print(e)

    def close_connection(self) -> None:
        """closes connection"""
        if self.conn:
            self.conn.close()

    def create_table(self) -> None:
        # Check if the table exists
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='MOVIES'")
        if self.cursor.fetchone() is None:
            # If the table does not exist, create it
            query = f'''CREATE TABLE MOVIES (
                id INTEGER PRIMARY KEY,
                Movie_Name TEXT,
                Tomato_Score TEXT,
                Audience_Score TEXT,
                storyline TEXT,
                rating TEXT,
                genres TEXT,
                review_1 TEXT,
                review_2 TEXT,
                review_3 TEXT,
                review_4 TEXT,
                review_5 TEXT,
                status TEXT
            )'''
            self.cursor.execute(query)
            self.conn.commit()
        else:
            # delete previous entries
            reset_sequence_query = "DELETE FROM MOVIES"
            self.cursor.execute(reset_sequence_query)
            self.conn.commit()


    def insert_to_database(self,MN,TS,AS,S,R,G,R1,R2,R3,R4,R5,status):

        insert_query = f'''INSERT INTO MOVIES
        (Movie_Name, Tomato_score,  Audience_score,  storyline, rating, genres, review_1, review_2, review_3, review_4, review_5, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''

        values = ( MN, TS, AS, S , R, G, R1, R2, R3, R4, R5,status)
        self.cursor.execute(insert_query,values)
        self.conn.commit()

