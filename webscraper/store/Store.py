import sqlite3
from typing import Dict

class Store(object):
    def __init__(self):
        self.con = sqlite3.connect("crawled.db")
        self.cur = self.con.cursor()

    def buildTable(self):
        self.cur.execute("CREATE TABLE paper(url, html)")

    def insertPapers(self, papers: Dict[str, str]):
        query = []
        for url, html in papers.items():
            query.append((url, html))

        self.cur.executemany("INSERT into paper VALUES(?, ?)", query)
        self.con.commit()

    def viewPapers(self):
        res = self.cur.execute("SELECT * FROM paper")
        print(res.fetchall())