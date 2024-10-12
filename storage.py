import sqlite3
import pandas as pd

class DBStorage():
    def __init__(self):
        self.con = sqlite3.connect("link.db")

    def setup_tables(self):
        cur = self.con.cursor()
        results_table = r"""
            CREATE TABLE IF NOT EXISTS results (
                id INTEGER PRIMARY KEY,
                query TEXT,
                rank INTEGER,
                link TEXT,
                title TEXT, 
                snippet TEXT,
                HTML,
                created DATETIME,
                relevance INTEGER, # Allows us to mark results as relevant or not relevant
                UNIQUE(query, link)
            );
        """

        cur.execute(results_table) # Execute code to create table
        self.con.commit()          # Commit changes 
        self.con.close()           # Close connection

    
    def query_results(self, query):
        df = pd.read_sql(f"select * from results where query='{query}' order by rank asc;", self.con)
        return df
    

    def insert_row(self, values):
        cur = self.con.cursor()
        try:
            cur.execute('INSERT INTO results (query, rank, link, title, snippet, html, created) VALUES (?,?,?,?,?,?,?)', values)
            self.con.commit()
        except sqlite3.IntegrityError: 
            pass

        cur.close()            