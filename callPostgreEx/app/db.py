from sqlalchemy import create_engine
from app import cfi2, cfi3, cfi4
import pyodbc
#import pyodbc as pyo

def connectSQL():
    """ Connect to the SQL database server """

    try:
        # read connection params
        con = cfi2        

        # connect to PostgreSQL server
        print('Connecting SQL...')
        engine = create_engine(con)       
        
        connection = engine.connect()

        return connection
    except:
        return print("Connection failed.")

def connectSQLDirect():
    """ Connect to the SQL database server """

    try:
        # read connection params
        con = cfi3       

        # connect to PostgreSQL server
        print('Connecting SQL...')
        #engine = create_engine(con)      
        conn = pyodbc.connect(con) 
        
        connection = conn

        return connection
    except:
        return print("Connection failed.")
    
def connectSQLVerify():
    """ Connect to the SQL database server """

    try:
        # read connection params
        con = cfi3        

        # connect to PostgreSQL server
        print('Connecting SQL...')
        engine = create_engine(con)       
        
        connection = engine.connect()

        return connection
    except:
        return print("Connection failed.")

def connectSQLnewRun():
    """ Connect to the SQL database server """

    try:
        # read connection params
        con = cfi4       
         
        # connect to PostgreSQL server
        print('Connecting SQL...')        
        engine = create_engine(con)       
        #conn = pyodbc.connect(con)
        connection = engine.connect()

        return connection
    except:
        return print("Connection failed.")

def connect():
    """ Connect to the PostgreSQL database server """

    try:
        # read connection params
        con = cfi1        

        # connect to PostgreSQL server
        print('Connecting...')
        engine = create_engine(con)       
        
        connection = engine.connect()

        return connection
    except:
        return print("Connection failed.")
    
def connectWrite():
    """ Connect to the PostgreSQL database server """

    try:
        # read connection params
        con = cfi1        

        # connect to PostgreSQL server
        print('Connecting...')
        engine = create_engine(con)       
        
        
        autocommit_engine = engine.execution_options(isolation_level="AUTOCOMMIT")

        connection = autocommit_engine.connect()

        return connection
    except:
        return print("Connection failed.")
    
def connectWriteSQL():
    """ Connect to the SQL database server """

    try:
        # read connection params
        con = cfi2

        # connect to PostgreSQL server
        print('Connecting SQL...')
        engine = create_engine(con)     

        autocommit_engine = engine.execution_options(isolation_level="AUTOCOMMIT")

        connection = autocommit_engine.connect()

        return connection
    except:
        return print("Connection failed.")

def connectSQLnewRunAutocommit():
    """ Connect to the SQL database server """

    try:
        # read connection params
        con = cfi4       
         
        # connect to PostgreSQL server
        print('Connecting SQL...')        
        engine = create_engine(con)       
        #conn = pyodbc.connect(con)
        connection = engine.connect()
        connection.autocommit = True
        return connection
    except:
        return print("Connection failed.")

# for debug
if __name__ == '__main__':
    #connection = connect()
    #connectionSQL = connectSQLnewRun()
    #connectionSQL = connectSQLnewRunAutocommit()
    connectionSQL = connectWriteSQL()
    result = connectionSQL.execute("SELECT @@VERSION;")
    for row in result:
        print(row)
    #connection.close()
    connectionSQL.close()