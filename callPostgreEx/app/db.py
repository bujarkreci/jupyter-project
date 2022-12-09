from sqlalchemy import create_engine
from app import cfi1, cfi2

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

# for debug
if __name__ == '__main__':
    #connection = connect()
    connectionSQL = connectSQL()
    result = connectionSQL.execute("SELECT @@VERSION;")
    for row in result:
        print(row)
    #connection.close()
    connectionSQL.close()