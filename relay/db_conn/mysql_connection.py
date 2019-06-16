
from mysql.connector import (connection) #MySQLConnector
from mysql.connector.cursor import MySQLCursorPrepared
import configparser
from os.path import expanduser

def read_config_file(filename = '.my.cnf', section = 'client'):
    parser = configparser.ConfigParser()
    #config_file = "{}/{}".format(expanduser("~"),filename)
    config_file = "/home/pi/{}".format(filename)
    #print(config_file)
    parser.read(config_file,encoding = "utf-8")
    
    data = {}

    if parser.has_section(section):
        items = parser.items(section)
        for item in items:
            data[item[0]] = item[1]
    else:
        raise Exception("{0} not found in {1}".format(section,config_file))

    #print(data)

    return data

class get_connection():
    def __init__(self):
        self.db_config = read_config_file()
        self.db_config['unix_socket']='/var/run/mysqld/mysqld.sock'
        #print(self.db_config)
        
        self.conn = connection.MySQLConnection(**self.db_config)
        self.curr = self.conn.cursor(cursor_class = MySQLCursorPrepared)
          
    def select_query(self,query):
        data = []
        columns = []
        error = []
        try:
            self.curr.execute(query)
            columns = self.curr.column_names
            data = self.fetchresults(columns,self.curr.fetchall())

        except Exception as e:
            error.append(e)
        return columns,data,error
    
    def select_params(self,query,params):
        columns = []
        data = []
        error = []
        
        try:
            self.curr.execute(query,params)
            columns = self.curr.column_names
            data = self.fetchresults(columns,self.curr.fetchall())
            
        except Exception as e:
            error.append(e)
        
        return columns,data,error
        
    def fetchresults(self,columns,query):
        data = []
        
        for recordset in query:
            c = 0
            d = {}
            for row_value in recordset:
                if type(row_value) == int:
                    d[columns[c]] = row_value
                else:
                    try:
                        d[columns[c]] = str(row_value.decode())
                    except:
                        d[columns[c]] = str(row_value)
                c += 1
            data.append(d)

        return data        
        
    def insert_query(self,query,params):

        self.curr.execute(query,params)
        self.conn.commit()
        return 'Data Inserted'
        
    def close_connection(self):
        self.conn.close()
        return 'Goodbye'
