import pymysql

class Database():
    def __init__(self):
        self.db = pymysql.connect(host='pomail.cylslqlklnx0.ap-northeast-2.rds.amazonaws.com',
                                  user='root',
                                  password='rootoor123',
                                  db='postfix_accounts',
                                  charset='utf8')
        self.cursor = self.db.cursor(pymysql.cursors.DictCursor)

    def execute(self, query, args={}):
        self.cursor.execute(query, args)

    def executeOne(self, query, args={}):
        self.cursor.execute(query, args)
        row = self.cursor.fetchone()
        return row

    def executeAll(self, query, args={}):
        self.cursor.execute(query, args)
        row = self.cursor.fetchall()
        return row

    def commit(self):
        self.db.commit()


