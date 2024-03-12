from decouple import config
from dotenv import load_dotenv
#import psycopg2 as pg
import pyodbc
import os

load_dotenv()

#secretKey = config("SECRET_KEY")
unamePostgre = config("PostgreUser")
passwPostgre = config("PostgrePass")

secretKey = os.environ.get('SECRET_KEY')
unameSQL = os.environ.get('SQLUser')
passwSQL = os.environ.get('SQLPass')
#unameSQL = config("SQLUser")
#passwSQL = config("SQLPass")

connPostgre = {
    'hostname' : '192.168.0.30',
    'database' : 'dellstore2',
    'username' : unamePostgre,
    'pwd' : passwPostgre,
    'port_id' : 5432
    }

connSQL = {
    'server' : '192.168.0.30', 
    'serverwithport' : '192.168.0.30,49172',
    'dbu' : 'NBAGame', 
    'uname' : unameSQL, 
    'passw' : passwSQL,
    'port' : '49172'
    }


class ConfigBase(object):
    
    SECRET_KEY = secretKey  

class ConfigPostgreSQL(ConfigBase):    
    conn = {
        "host" : connPostgre['hostname'],
        "dbname" : connPostgre['database'],
        "user" : connPostgre['username'],
        "password" : connPostgre['pwd'],
        "port" : connPostgre['port_id']
    }
#url = 'mssql+pyodbc://{user}:{passwd}@{host}:{port}/{db}?driver=SQL+Server'.format(user=username, passwd=password, host=host, port=port, db=database)    
class ConfigPostgreSQLAlchemy(ConfigBase):    
    par = 'postgresql://' + connPostgre['username'] + ':' + connPostgre['pwd'] + '@' + connPostgre['hostname'] + ':' + str(connPostgre['port_id']) + '/' + connPostgre['database']        
#connSqlServer = pyodbc.connect('DRIVER={SQL Server Native Client 10.0};SERVER=192.106.0.102,1443;DATABASE=master;UID=sql2008;PWD=password123')    
class ConfigSQLnewestODBC(ConfigBase):
    par = 'mssql+pyodbc://{user}:{passwd}@{host}:{port}/{db}?driver=SQL+Server'.format(user=connSQL['uname'], passwd=connSQL['passw'], host=connSQL['server'], port=connSQL['port'], db=connSQL['dbu'])

class ConfigSQLAlchemy(ConfigBase):
    par = "mssql+pyodbc://" + connSQL['uname'] + ":" + connSQL['passw'] + "@" + connSQL['server'] + ":" + str(connSQL['port']) + "/" + connSQL['dbu'] + "?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes"
    
#This ConfigSQLDirect is not working need further to investigate
class ConfigSQLDirect(ConfigBase):
    cnxn = ("Driver={SQL Server Native Client 11.0};"
            f"Server={connSQL['serverwithport']};"
            f"Database={connSQL['dbu']};"
            f"UID={connSQL['uname']};"
            f"PWD={connSQL['passw']};")

config = {    
    'PostgreSQL': ConfigPostgreSQL.conn,
    'PostgreSQLalchemy' : ConfigPostgreSQLAlchemy.par,
    'SQLAlchemy' : ConfigSQLAlchemy.par,
    'SQLDirect' : ConfigSQLDirect.cnxn,
    'SQLveryodbcdbc' : ConfigSQLnewestODBC.par
}